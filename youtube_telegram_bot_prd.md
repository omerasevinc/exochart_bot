# YouTube Live Frame Capture Telegram Bot - PRD & Implementation Guide

## Product Requirements Document (PRD)

### 1. Project Overview
**Product Name:** YouTube Live Frame Capture Telegram Bot  
**Purpose:** Capture and send live video frames from YouTube streams via Telegram bot commands  
**Target User:** Individual user wanting real-time frame captures from specific YouTube live streams

### 2. Core Requirements

#### 2.1 Functional Requirements
- **Trigger Command:** Bot responds to specific message (e.g., "btc")
- **Frame Capture:** Extract current frame from YouTube live stream using yt-dlp + ffmpeg
- **Image Delivery:** Send captured frame as image via Telegram
- **Error Handling:** Graceful handling of stream offline/unavailable scenarios
- **Configuration:** Easy setup for different YouTube live streams

#### 2.2 Technical Requirements
- **Dependencies:** yt-dlp, ffmpeg, python-telegram-bot
- **Platform:** Cross-platform (Linux/Windows/macOS)
- **Storage:** Temporary frame storage with automatic cleanup
- **Response Time:** Frame capture and delivery within 30 seconds
- **Format:** JPEG/PNG image output

#### 2.3 Non-Functional Requirements
- **Reliability:** 95% uptime for frame capture when stream is live
- **Performance:** Handle multiple capture requests efficiently
- **Security:** Secure Telegram bot token management
- **Maintainability:** Modular code structure for easy updates

### 3. User Stories
1. **As a user**, I want to send "btc" to my Telegram bot and receive the current frame from a YouTube live stream
2. **As a user**, I want to be notified if the stream is offline or unavailable
3. **As a user**, I want the bot to respond quickly with high-quality frame captures

### 4. Technical Architecture

#### 4.1 Components
- **Telegram Bot Handler:** Processes incoming messages and commands
- **YouTube Stream Manager:** Handles yt-dlp operations and stream URL resolution
- **Frame Capture Engine:** Uses ffmpeg to extract frames
- **File Manager:** Handles temporary file creation and cleanup
- **Configuration Manager:** Manages bot settings and stream URLs

#### 4.2 Data Flow
1. User sends trigger message to Telegram bot
2. Bot validates command and initiates frame capture
3. yt-dlp resolves YouTube live stream URL
4. ffmpeg captures current frame
5. Bot sends image to user via Telegram
6. Temporary files cleaned up

---

## Step-by-Step Implementation Guide

### Step 1: Environment Setup

#### 1.1 Install Required Dependencies
```bash
# Install Python packages
pip install python-telegram-bot yt-dlp

# Install ffmpeg (system-level)
# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# macOS (with Homebrew):
brew install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

#### 1.2 Create Project Structure
```
youtube_telegram_bot/
├── main.py
├── config.py
├── bot_handler.py
├── frame_capture.py
├── utils.py
├── requirements.txt
└── temp_frames/
```

### Step 2: Configuration Setup

#### 2.1 Create config.py
```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    ALLOWED_USER_IDS = [int(x) for x in os.getenv('ALLOWED_USER_IDS', '').split(',') if x]
    
    # YouTube Configuration
    YOUTUBE_LIVE_URL = os.getenv('YOUTUBE_LIVE_URL', 'https://youtube.com/watch?v=YOUR_LIVE_STREAM_ID')
    
    # Trigger Commands
    TRIGGER_COMMANDS = ['btc', 'capture', 'frame']
    
    # File Management
    TEMP_DIR = 'temp_frames'
    IMAGE_FORMAT = 'jpg'
    IMAGE_QUALITY = 85
    
    # Timeouts (seconds)
    YTDLP_TIMEOUT = 30
    FFMPEG_TIMEOUT = 20
    
    # FFmpeg Configuration
    FFMPEG_OPTIONS = {
        'vframes': 1,
        'q:v': 2,
        'vf': 'scale=1280:720'  # Resize to 720p
    }
```

### Step 3: Frame Capture Implementation

#### 3.1 Create frame_capture.py
```python
import subprocess
import tempfile
import os
import logging
from typing import Optional, Tuple
import yt_dlp
from config import Config

logger = logging.getLogger(__name__)

class FrameCaptureEngine:
    def __init__(self, config: Config):
        self.config = config
        self.ensure_temp_dir()
    
    def ensure_temp_dir(self):
        """Create temporary directory if it doesn't exist"""
        os.makedirs(self.config.TEMP_DIR, exist_ok=True)
    
    def get_live_stream_url(self, youtube_url: str) -> Optional[str]:
        """Extract actual stream URL using yt-dlp"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best[ext=mp4]/best',
            'socket_timeout': self.config.YTDLP_TIMEOUT,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                if info and 'url' in info:
                    return info['url']
                else:
                    logger.error("No stream URL found")
                    return None
        except Exception as e:
            logger.error(f"yt-dlp error: {e}")
            return None
    
    def capture_frame(self, stream_url: str) -> Tuple[Optional[str], Optional[str]]:
        """Capture frame using ffmpeg"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=f'.{self.config.IMAGE_FORMAT}',
                dir=self.config.TEMP_DIR,
                delete=False
            )
            temp_file.close()
            
            # Build ffmpeg command
            cmd = [
                'ffmpeg',
                '-i', stream_url,
                '-vframes', str(self.config.FFMPEG_OPTIONS['vframes']),
                '-q:v', str(self.config.FFMPEG_OPTIONS['q:v']),
                '-vf', self.config.FFMPEG_OPTIONS['vf'],
                '-y',  # Overwrite output file
                temp_file.name
            ]
            
            # Execute ffmpeg command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.FFMPEG_TIMEOUT
            )
            
            if result.returncode == 0 and os.path.exists(temp_file.name):
                return temp_file.name, None
            else:
                error_msg = f"FFmpeg failed: {result.stderr}"
                logger.error(error_msg)
                self.cleanup_file(temp_file.name)
                return None, error_msg
                
        except subprocess.TimeoutExpired:
            error_msg = "Frame capture timed out"
            logger.error(error_msg)
            return None, error_msg
        except Exception as e:
            error_msg = f"Frame capture error: {e}"
            logger.error(error_msg)
            return None, error_msg
    
    def cleanup_file(self, file_path: str):
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {e}")
    
    async def capture_and_get_frame(self, youtube_url: str) -> Tuple[Optional[str], Optional[str]]:
        """Main method to capture frame from YouTube live stream"""
        # Step 1: Get actual stream URL
        logger.info("Resolving YouTube live stream URL...")
        stream_url = self.get_live_stream_url(youtube_url)
        
        if not stream_url:
            return None, "Failed to resolve YouTube stream URL. Stream might be offline."
        
        # Step 2: Capture frame
        logger.info("Capturing frame from stream...")
        frame_path, error = self.capture_frame(stream_url)
        
        return frame_path, error
```

### Step 4: Telegram Bot Handler

#### 4.1 Create bot_handler.py
```python
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from frame_capture import FrameCaptureEngine
from config import Config

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    def __init__(self, config: Config):
        self.config = config
        self.frame_engine = FrameCaptureEngine(config)
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Message handlers for trigger words
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    def is_authorized_user(self, user_id: int) -> bool:
        """Check if user is authorized"""
        if not self.config.ALLOWED_USER_IDS:
            return True  # If no restrictions set, allow all users
        return user_id in self.config.ALLOWED_USER_IDS
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not self.is_authorized_user(update.effective_user.id):
            await update.message.reply_text("❌ You are not authorized to use this bot.")
            return
        
        welcome_msg = (
            "🤖 YouTube Live Frame Capture Bot\n\n"
            f"Send any of these commands to capture a frame:\n"
            f"• {', '.join(self.config.TRIGGER_COMMANDS)}\n\n"
            "Use /help for more information."
        )
        await update.message.reply_text(welcome_msg)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not self.is_authorized_user(update.effective_user.id):
            await update.message.reply_text("❌ You are not authorized to use this bot.")
            return
        
        help_msg = (
            "📖 **Help - YouTube Frame Capture Bot**\n\n"
            "**Available Commands:**\n"
            f"• `{', '.join(self.config.TRIGGER_COMMANDS)}` - Capture current frame\n"
            "• `/start` - Show welcome message\n"
            "• `/help` - Show this help\n\n"
            "**How it works:**\n"
            "1. Send a trigger command\n"
            "2. Bot captures current frame from YouTube live stream\n"
            "3. Frame is sent as image\n\n"
            "⚡ Response time: ~10-30 seconds"
        )
        await update.message.reply_text(help_msg, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        if not self.is_authorized_user(update.effective_user.id):
            await update.message.reply_text("❌ You are not authorized to use this bot.")
            return
        
        message_text = update.message.text.lower().strip()
        
        # Check if message matches trigger commands
        if message_text in [cmd.lower() for cmd in self.config.TRIGGER_COMMANDS]:
            await self.capture_and_send_frame(update, context)
    
    async def capture_and_send_frame(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Capture frame and send to user"""
        # Send initial status message
        status_msg = await update.message.reply_text("📸 Capturing frame from live stream...")
        
        try:
            # Capture frame
            frame_path, error = await self.frame_engine.capture_and_get_frame(
                self.config.YOUTUBE_LIVE_URL
            )
            
            if frame_path:
                # Send image
                await update.message.reply_photo(
                    photo=open(frame_path, 'rb'),
                    caption="📸 Live stream frame captured!"
                )
                
                # Cleanup temporary file
                self.frame_engine.cleanup_file(frame_path)
                
                # Delete status message
                await status_msg.delete()
                
            else:
                # Send error message
                error_text = f"❌ Frame capture failed:\n{error}"
                await status_msg.edit_text(error_text)
                
        except Exception as e:
            logger.error(f"Error in capture_and_send_frame: {e}")
            await status_msg.edit_text(f"❌ An error occurred: {str(e)}")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        self.application.run_polling()
```

### Step 5: Main Application

#### 5.1 Create main.py
```python
import logging
import os
from config import Config
from bot_handler import TelegramBotHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    # Load configuration
    config = Config()
    
    # Validate configuration
    if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("Please set your TELEGRAM_BOT_TOKEN in environment variables or config.py")
        return
    
    if not config.YOUTUBE_LIVE_URL or 'YOUR_LIVE_STREAM_ID' in config.YOUTUBE_LIVE_URL:
        logger.error("Please set your YOUTUBE_LIVE_URL in environment variables or config.py")
        return
    
    # Create and start bot
    try:
        bot = TelegramBotHandler(config)
        logger.info("YouTube Live Frame Capture Bot is starting...")
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    main()
```

### Step 6: Requirements File

#### 6.1 Create requirements.txt
```txt
python-telegram-bot==20.7
yt-dlp==2023.12.30
```

### Step 7: Deployment Instructions

#### 7.1 Environment Variables Setup
```bash
# Create .env file (optional)
export TELEGRAM_BOT_TOKEN="your_bot_token_from_botfather"
export YOUTUBE_LIVE_URL="https://youtube.com/watch?v=your_live_stream_id"
export ALLOWED_USER_IDS="your_telegram_user_id"  # Optional: comma-separated IDs
```

#### 7.2 Running the Bot
```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

### Step 8: Testing & Verification

#### 8.1 Test Checklist
- [ ] Bot responds to /start command
- [ ] Bot responds to trigger commands (btc, capture, frame)
- [ ] Frame capture works when stream is live
- [ ] Error handling works when stream is offline
- [ ] Image quality is acceptable
- [ ] Response time is under 30 seconds
- [ ] Temporary files are cleaned up

#### 8.2 Troubleshooting
1. **Bot not responding:** Check bot token and network connectivity
2. **yt-dlp errors:** Verify YouTube URL and stream availability
3. **ffmpeg errors:** Ensure ffmpeg is installed and accessible
4. **Permission errors:** Check file permissions in temp directory
5. **Timeout errors:** Adjust timeout values in config

### Step 9: Production Considerations

#### 9.1 Monitoring & Logging
- Implement log rotation
- Add health check endpoints
- Monitor error rates and response times

#### 9.2 Scalability
- Consider rate limiting for multiple users
- Implement caching for frequently accessed streams
- Add database for configuration management

#### 9.3 Security
- Use environment variables for sensitive data
- Implement user authentication/authorization
- Regular dependency updates

---

## Quick Start Summary

1. **Setup:** Install Python, ffmpeg, and dependencies
2. **Configure:** Set bot token and YouTube URL in config.py
3. **Run:** Execute `python main.py`
4. **Test:** Send "btc" to your bot via Telegram
5. **Enjoy:** Receive live stream frames instantly!

**Estimated Setup Time:** 15-30 minutes  
**Technical Level:** Intermediate