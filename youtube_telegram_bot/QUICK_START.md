# 🚀 Quick Start Guide - YouTube Live Frame Capture Bot

## ✅ Current Status: Ready to Configure & Run!

All dependencies are installed and tests passed! You just need to configure your bot token and YouTube URL.

## 📋 Prerequisites (✅ Already Done)

- ✅ Python 3.7+ (detected)
- ✅ Virtual environment created
- ✅ Dependencies installed (python-telegram-bot, yt-dlp)
- ✅ FFmpeg available at `/opt/homebrew/bin/ffmpeg`
- ✅ All modules tested and working

## 🔧 Configuration (Next Steps)

### 1. Create Your Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Choose a name: `YouTube Frame Bot` (or any name you like)
4. Choose a username: `your_frame_bot` (must end with 'bot')
5. Copy the bot token that looks like: `123456789:ABCDefGHIjklMNOPqrsTUVwxyz`

### 2. Get YouTube Live Stream URL

Find a YouTube live stream URL like:
- `https://youtube.com/watch?v=VIDEO_ID`
- For testing, you can use any live stream (news channels, etc.)

### 3. Configure the Bot

```bash
# Copy the template
cp env_template.txt .env

# Edit the .env file
nano .env
```

Edit `.env` with your values:
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklMNOPqrsTUVwxyz
YOUTUBE_LIVE_URL=https://youtube.com/watch?v=YOUR_VIDEO_ID
ALLOWED_USER_IDS=  # Optional: your telegram user ID
```

## 🚀 Run the Bot

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the bot
python main.py
```

You should see:
```
INFO - YouTube Live Frame Capture Bot is starting...
INFO - Starting Telegram bot...
```

## 📱 Test the Bot

1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send `btc` to capture a frame
4. Bot will respond with: "📸 Capturing frame from live stream..."
5. You'll receive the captured frame image!

## 🔄 Commands to Remember

**When you restart your terminal, always activate the virtual environment first:**

```bash
cd /Users/omersevinc/Documents/exochart_bot/youtube_telegram_bot
source venv/bin/activate
python main.py
```

## 🛠️ Troubleshooting

### Bot Token Issues
- Make sure token has no extra spaces
- Verify you copied the full token from BotFather

### YouTube URL Issues  
- Use a currently live stream
- Make sure URL is accessible
- Try a different live stream if one isn't working

### Virtual Environment Issues
```bash
# If venv folder gets deleted, recreate it:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎯 Bot Commands (Once Running)

Send these to your bot:
- `/start` - Welcome message
- `/help` - Help information
- `btc` - Capture frame
- `capture` - Capture frame  
- `frame` - Capture frame

---

## 🎉 You're All Set!

The bot is ready to capture YouTube live frames and send them via Telegram. Just configure your bot token and YouTube URL, then run it!