# Primr Slack Assistant

A conversational AI assistant that integrates with Slack to answer questions about your company documentation using retrieval-augmented generation (RAG).

## Features

- **Document Search**: Semantic search through your markdown documents
- **AI Responses**: Uses OpenAI GPT models for intelligent answers
- **Vector Storage**: Local FAISS or cloud Pinecone options
- **Slack Integration**: Ready for Slack bot deployment

## Prerequisites

- Python 3.9+ (Python 3.13 not supported by faiss-cpu yet)
- OpenAI API key
- macOS (for this setup guide)

## Installation & Setup

### 1. Install Dependencies

```bash
# Navigate to project directory
cd /Users/shaesmith/Documents/Primr/primr-slack-assistant

# Create virtual environment
python -m venv primr-bot-env

# Activate virtual environment
source primr-bot-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
# Slack Bot Configuration (required for Slack integration)
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
# Optional: only if using Pinecone
#PINECONE_API_KEY=your-pinecone-key
#PINECONE_ENVIRONMENT=your-pinecone-env
```

**⚠️ CRITICAL SECURITY**:
1. **FIRST** create `.gitignore` with `.env` in it
2. **THEN** create your `.env` file
3. **NEVER** commit API keys to version control
4. If you accidentally expose keys, **immediately revoke and create new ones**

```bash
# Verify .env is ignored before committing
git status  # .env should NOT appear in the list
```

### 3. Get OpenAI API Key

1. Visit [platform.openai.com](https://platform.openai.com)
2. Create account and add billing method
3. Go to API Keys → Create new secret key
4. Copy key to your `.env` file

## Usage

### Step 1: Prepare Documents

Add your markdown files to the `data/` folder:

```bash
mkdir data
# Add your .md files: data/policies.md, data/benefits.md, etc.
```

### Step 2: Process Documents

Always activate your virtual environment first:

```bash
source primr-bot-env/bin/activate
```

Chunk your documents:

```bash
python ingest.py
```

This creates `chunks.json` with processed document chunks.

### Step 3: Build Vector Index

Create the searchable embeddings:

```bash
python build_story.py
```

This creates a `faiss_index/` directory with your vector database.

### Step 4: Test the System

Run the interactive query interface:

```bash
python query.py
```

Ask questions about your documents!

## Complete Workflow Example

```bash
# 1. Activate environment
source primr-bot-env/bin/activate

# 2. Add sample document
echo "# Company Policies\nOur vacation policy allows 3 weeks PTO..." > data/policies.md

# 3. Process documents
python ingest.py
# Output: 🔖 X chunks saved to chunks.json

# 4. Build vector index
python build_story.py
# Output: 💾 FAISS index saved to ./faiss_index/

# 5. Test queries
python query.py
# Ask: "What is the vacation policy?"
```

## Troubleshooting

### Common Issues

**Import errors**:
```bash
# Make sure you're in the right environment
source primr-bot-env/bin/activate
python your_script.py
```

**OpenAI API errors**:
- Check your API key is correct in `.env`
- Verify billing is set up at platform.openai.com
- Ensure you have credits remaining

**No documents found**:
```bash
# Make sure you have .md files in data/
ls data/
# Should show your markdown files
```

## Slack Integration

### Quick Start
1. **Set up Slack App**: Follow the detailed guide in [`SLACK_SETUP.md`](SLACK_SETUP.md)
2. **Add tokens to `.env`**:
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   SLACK_APP_TOKEN=xapp-your-app-token-here
   ```
3. **Start the bot**:
   ```bash
   source primr-bot-env/bin/activate
   python slack_bot.py
   ```

### Daily Workflow
```bash
# Every time you work on the project:
cd /Users/shaesmith/Documents/Primr/primr-slack-assistant
source primr-bot-env/bin/activate
python slack_bot.py

# To deactivate when done:
deactivate
```
