import os
import subprocess
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Initialize Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Initialize AI components (lazy loading for better startup time)
qa_chain = None

def get_qa_chain():
    """Lazy load the QA chain to improve startup time"""
    global qa_chain
    if qa_chain is None:
        print("🔄 Loading AI components...")

        try:
            # Check if vector index exists
            if not os.path.exists("faiss_index"):
                raise FileNotFoundError("Vector index not found. Please add documents to data/ folder and restart the bot.")

            # Load FAISS index
            vs = FAISS.load_local(
                "faiss_index",
                OpenAIEmbeddings(model="text-embedding-ada-002"),
                allow_dangerous_deserialization=True
            )

            retriever = vs.as_retriever(search_kwargs={"k": 5})

            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(model="gpt-4", temperature=0),
                chain_type="stuff",
                retriever=retriever,
            )

            print("✅ AI components loaded!")

        except Exception as e:
            print(f"❌ Failed to load AI components: {e}")
            raise

    return qa_chain

# Message handler for DMs only (not mentions)
@app.message(".*")
def handle_message(message, say):
    """Handle direct messages to the bot (not mentions)"""
    # Skip if this is a mention (handled by app_mention event)
    if f"<@{app.client.auth_test()['user_id']}>" in message.get('text', ''):
        return

    try:
        user_query = message['text']

        if not user_query.strip():
            say("👋 Hi! I'm Primr Assistant. Ask me anything about our company documents!")
            return

        # Show typing indicator
        say("🔍 Searching our knowledge base...")

        # Get AI response
        qa = get_qa_chain()
        result = qa.invoke({"query": user_query})
        answer = result["result"]

        # Send response
        say(f"💡 {answer}")

    except FileNotFoundError as e:
        say("📁 I don't have any documents to search yet. Please ask an admin to add some company documents!")
    except Exception as e:
        print(f"Error handling message: {e}")
        say("😅 I'm having some technical difficulties. Please try again in a moment!")

# Slash command handler
@app.command("/ask-primr")
def handle_ask_command(ack, respond, command):
    """Handle /ask-primr slash command"""
    ack()

    try:
        user_query = command['text'].strip()

        if not user_query:
            respond("Please provide a question! Example: `/ask-primr What is our vacation policy?`")
            return

        # Show immediate response so user knows bot is working
        respond("🔍 Searching our knowledge base...")

        # Get AI response
        qa = get_qa_chain()
        result = qa.invoke({"query": user_query})
        answer = result["result"]

        # Send follow-up with the answer
        app.client.chat_postMessage(
            channel=command['channel_id'],
            text=f"💡 **Answer to:** {user_query}\n\n{answer}"
        )

    except FileNotFoundError as e:
        respond("📁 I don't have any documents to search yet. Please ask an admin to add some company documents!")
    except Exception as e:
        print(f"Error handling slash command: {e}")
        respond("😅 Sorry, I encountered an error. Please try again!")

# App mention handler (when someone @mentions the bot)
@app.event("app_mention")
def handle_app_mention(event, say):
    """Handle when the bot is mentioned"""
    try:
        user_query = event['text']

        # Remove bot mention
        user_id = app.client.auth_test()["user_id"]
        user_query = user_query.replace(f"<@{user_id}>", "").strip()

        if not user_query:
            say("👋 Hi! I'm Primr Assistant. Ask me anything about our company documents!")
            return

        # Show typing indicator
        say("🔍 Searching our knowledge base...")

        # Get AI response
        qa = get_qa_chain()
        result = qa.invoke({"query": user_query})
        answer = result["result"]

        say(f"💡 {answer}")

    except FileNotFoundError as e:
        say("📁 I don't have any documents to search yet. Please ask an admin to add some company documents!")
    except Exception as e:
        print(f"Error handling mention: {e}")
        say("😅 I'm having some technical difficulties. Please try again in a moment!")

# Health check command
@app.command("/primr-status")
def handle_status_command(ack, respond):
    """Check bot status"""
    ack()

    try:
        # Check if AI components are loaded
        if qa_chain is None:
            respond("🟡 Bot is running but AI components not loaded yet. Send a message to initialize!")
        else:
            respond("🟢 Bot is running and ready to answer questions!")

    except Exception as e:
        respond(f"🔴 Bot error: {e}")

# Bot startup message - only handle DMs that aren't mentions
@app.event("message", matchers=[lambda message: message.get("channel_type") == "im"])
def handle_direct_message(message, say):
    """Handle direct messages to the bot"""
    # Only process if it's a DM and has text, and skip if it's already handled
    if message.get("text") and f"<@{app.client.auth_test()['user_id']}>" not in message.get('text', ''):
        handle_message(message, say)

if __name__ == "__main__":
    print("🚀 Starting Primr Slack Assistant...")

    # Check for required environment variables
    missing_vars = []
    if not os.environ.get("SLACK_BOT_TOKEN"):
        missing_vars.append("SLACK_BOT_TOKEN")
    if not os.environ.get("SLACK_APP_TOKEN"):
        missing_vars.append("SLACK_APP_TOKEN")
    if not os.environ.get("OPENAI_API_KEY"):
        missing_vars.append("OPENAI_API_KEY")

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📖 See SLACK_SETUP.md for configuration instructions")
        exit(1)

    # Check for vector index
    if not os.path.exists("faiss_index"):
        print("⚠️  Vector index not found. Auto-building from available documents...")
        try:
            subprocess.run(["python", "ingest.py"], check=True)
            subprocess.run(["python", "build_story.py"], check=True)
            print("✅ Vector index built successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to build vector index. Please run 'python ingest.py' and 'python build_story.py' manually")
            exit(1)
        except FileNotFoundError:
            print("❌ No documents found in data/ folder. Please add some .md files and try again")
            exit(1)

    print("✅ All systems ready!")
    print("🤖 Bot will respond to:")
    print("   • Direct messages")
    print("   • @mentions in channels")
    print("   • /ask-primr slash command")

    # Start the app
    try:
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        handler.start()
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        print("📖 Check SLACK_SETUP.md for troubleshooting")