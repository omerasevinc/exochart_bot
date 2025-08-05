#!/bin/bash
# Quick script to run the YouTube Live Frame Capture Bot

echo "🤖 YouTube Live Frame Capture Bot - Startup Script"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run setup first: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [ -f "env_template.txt" ]; then
        cp env_template.txt .env
        echo "📝 Created .env file from template"
        echo "⚠️  Please edit .env file with your bot token and YouTube URL before running again"
        echo "   nano .env"
        exit 1
    else
        echo "❌ env_template.txt not found!"
        exit 1
    fi
fi

# Check configuration
echo "🔧 Checking configuration..."
python -c "
from config import Config
config = Config()

if config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    print('❌ TELEGRAM_BOT_TOKEN not configured')
    print('Please edit .env file with your bot token')
    exit(1)

if 'YOUR_LIVE_STREAM_ID' in config.YOUTUBE_LIVE_URL:
    print('❌ YOUTUBE_LIVE_URL not configured') 
    print('Please edit .env file with your YouTube URL')
    exit(1)

print('✅ Configuration looks good!')
"

# Check if configuration validation passed
if [ $? -ne 0 ]; then
    echo ""
    echo "Please configure your bot:"
    echo "1. Edit .env file: nano .env"
    echo "2. Add your bot token from @BotFather"
    echo "3. Add your YouTube live stream URL"
    echo "4. Run this script again: ./run_bot.sh"
    exit 1
fi

# Run the bot
echo "🚀 Starting bot..."
echo "Press Ctrl+C to stop"
echo ""
python main.py