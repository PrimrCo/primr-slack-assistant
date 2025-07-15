# Slack App Setup Guide

This guide will walk you through setting up your Slack app to work with the Primr Assistant.

## Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click the green **"Create New App"** button
3. Choose **"From scratch"** (not from manifest)
4. Enter app details:
   - **App Name**: "Primr Assistant" (or your preferred name)
   - **Pick a workspace**: Select your workspace from the dropdown
5. Click **"Create App"**

## Step 2: Configure Bot Permissions

### OAuth & Permissions
1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll down to the **"Scopes"** section
3. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"** for each:
   - `app_mentions:read` - View messages that directly mention @your_bot
   - `channels:history` - View messages and other content in public channels
   - `chat:write` - Send messages as your app
   - `im:history` - View messages and other content in direct messages
   - `im:write` - Start direct messages with people
   - `commands` - Add shortcuts and/or slash commands

### Install App to Workspace
1. Scroll up to the **"OAuth Tokens for Your Workspace"** section
2. Click the green **"Install to Workspace"** button
3. Review permissions and click **"Allow"**
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)
5. Paste it in your `.env` file as `SLACK_BOT_TOKEN=xoxb-your-token-here`

## Step 3: Enable Socket Mode

1. In the left sidebar, click **"Socket Mode"**
2. Toggle **"Enable Socket Mode"** to **ON**
3. In the popup, enter a token name like "primr-socket-token"
4. Click **"Generate"**
5. Copy the **"App-Level Token"** (starts with `xapp-`)
6. Paste it in your `.env` file as `SLACK_APP_TOKEN=xapp-your-token-here`

## Step 4: Configure Slash Commands

1. In the left sidebar, click **"Slash Commands"**
2. Click the **"Create New Command"** button
3. Set up the first command:
   - **Command**: `/ask-primr`
   - **Request URL**: Leave this blank (Socket Mode handles it)
   - **Short Description**: Ask Primr Assistant a question about company docs
   - **Usage Hint**: What is our vacation policy?
   - Click **"Save"**

4. Click **"Create New Command"** again for the status command:
   - **Command**: `/primr-status`
   - **Request URL**: Leave blank
   - **Short Description**: Check if Primr Assistant is running and ready
   - **Usage Hint**: (leave empty)
   - Click **"Save"**

## Step 5: Configure Event Subscriptions

1. In the left sidebar, click **"Event Subscriptions"**
2. Toggle **"Enable Events"** to **ON**
3. Under **"Subscribe to bot events"**, click **"Add Bot User Event"** for each:
   - `app_mention` - Subscribe to only the message events that mention your app
   - `message.channels` - A message was posted to a channel (if bot is added to channel)
   - `message.im` - A message was posted in a direct message channel
4. Click **"Save Changes"** at the bottom

## Step 6: Your .env File Should Look Like:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

## Step 7: Test Your Bot

1. **The bot will auto-setup**: Just start it and it will build the vector index automatically if needed:
   ```bash
   conda activate faiss-env
   python slack_bot.py
   ```

   You should see:
   ```
   🚀 Starting Primr Slack Assistant...
   ✅ All systems ready!
   🤖 Bot will respond to:
      • Direct messages
      • @mentions in channels
      • /ask-primr slash command
   ```

2. **Test in Slack**:
   - **Direct message**: Send a DM to your bot: "What is our vacation policy?"
   - **Channel mention**: Add bot to channel first, then: "@Primr Assistant help me with expenses"
   - **Slash command**: Works anywhere: `/ask-primr What are our benefits?`
   - **Status check**: Type `/primr-status` to verify bot is working

   > **Note**: For @mentions in channels, you must first add the bot to the channel by typing `/invite @Primr Assistant` or going to channel settings → Integrations → Add apps.

## Troubleshooting

### Bot doesn't respond
- **Check tokens**: Verify both `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` are correct in `.env`
- **Restart bot**: Stop with Ctrl+C and run `python slack_bot.py` again
- **Check documents**: Make sure you have `.md` files in the `data/` folder
- **Bot permissions**: Ensure bot is added to the channel where you're testing

### "Permission denied" or scope errors
- **Add missing scopes**: Go back to OAuth & Permissions and add any missing scopes
- **Reinstall app**: After adding scopes, click "Reinstall to Workspace"
- **Bot token**: Make sure you're using the Bot User OAuth Token, not User OAuth Token

### Socket mode connection issues
- **Verify Socket Mode**: Make sure it's enabled and you have a valid App-Level Token
- **Network/firewall**: Ensure your network allows WebSocket connections
- **Token format**: App-Level Token should start with `xapp-`

### Bot gives "no documents" error
- **Add documents**: Put some `.md` files in the `data/` folder
- **Auto-build**: The bot will automatically process them on startup
- **Manual build**: Or run `python ingest.py && python build_story.py` manually

## Next Steps

Once working, you can:
1. Add the bot to specific channels
2. Customize the responses and personality
3. Add more slash commands
4. Deploy to a server for 24/7 availability
