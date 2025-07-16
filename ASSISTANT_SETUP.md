# Quick Setup Guide

## Environment Setup

### 1. Create Virtual Environment
```bash
cd /Users/shaesmith/Documents/Primr/primr-slack-assistant
python -m venv primr-bot-env
source primr-bot-env/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Ensure your `.env` file contains:
```
OPENAI_API_KEY=your_openai_key_here
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

### 4. Run the Bot
```bash
python slack_bot.py
```

## Daily Workflow
```bash
# Activate environment
source primr-bot-env/bin/activate

# Run bot
python slack_bot.py

# Deactivate when done
deactivate
```

## Adding New Dependencies
```bash
# Activate environment first
source primr-bot-env/bin/activate

# Install new package
pip install new-package-name

# Update requirements.txt
pip freeze > requirements.txt
```
### Quick Steps
```bash
cd /Users/shaesmith/Documents/Primr/primr-slack-assistant
source primr-bot-env/bin/activate
python slack_bot.py
```
