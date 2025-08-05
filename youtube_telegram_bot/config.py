import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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