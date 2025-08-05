#!/usr/bin/env python3
"""
Test script to verify the bot setup without actually running it
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-telegram-bot: {e}")
        return False
    
    try:
        import yt_dlp
        print("✅ yt-dlp imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import yt-dlp: {e}")
        return False
    
    return True

def test_local_modules():
    """Test if local modules can be imported"""
    print("\n🧪 Testing local modules...")
    
    try:
        from config import Config
        print("✅ config.py imported successfully")
        
        config = Config()
        print(f"✅ Configuration loaded")
        print(f"   - Trigger commands: {config.TRIGGER_COMMANDS}")
        print(f"   - Image format: {config.IMAGE_FORMAT}")
        print(f"   - Temp directory: {config.TEMP_DIR}")
        
    except Exception as e:
        print(f"❌ Failed to import config: {e}")
        return False
    
    try:
        from frame_capture import FrameCaptureEngine
        print("✅ frame_capture.py imported successfully")
        
        engine = FrameCaptureEngine(config)
        print("✅ FrameCaptureEngine instantiated")
        
    except Exception as e:
        print(f"❌ Failed to import frame_capture: {e}")
        return False
    
    try:
        from bot_handler import TelegramBotHandler
        print("✅ bot_handler.py imported successfully")
        
    except Exception as e:
        print(f"❌ Failed to import bot_handler: {e}")
        return False
    
    try:
        from utils import validate_youtube_url, is_ffmpeg_available
        print("✅ utils.py imported successfully")
        
        # Test utility functions
        print(f"✅ FFmpeg available: {is_ffmpeg_available()}")
        print(f"✅ YouTube URL validation works: {validate_youtube_url('https://youtube.com/watch?v=test')}")
        
    except Exception as e:
        print(f"❌ Failed to import utils: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'main.py',
        'config.py',
        'bot_handler.py',
        'frame_capture.py',
        'utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    # Check temp directory
    if Path('temp_frames').exists():
        print("✅ temp_frames directory exists")
    else:
        print("❌ temp_frames directory missing")
        all_exist = False
    
    return all_exist

def test_configuration():
    """Test configuration validity"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config import Config
        config = Config()
        
        # Check if configuration has been updated
        if config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("⚠️  TELEGRAM_BOT_TOKEN not configured")
        else:
            print("✅ TELEGRAM_BOT_TOKEN is set")
        
        if 'YOUR_LIVE_STREAM_ID' in config.YOUTUBE_LIVE_URL:
            print("⚠️  YOUTUBE_LIVE_URL not configured")
        else:
            print("✅ YOUTUBE_LIVE_URL is set")
        
        # Test other configuration values
        if config.TRIGGER_COMMANDS:
            print(f"✅ Trigger commands configured: {config.TRIGGER_COMMANDS}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 YouTube Live Frame Capture Bot - Setup Test")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_local_modules,
        test_configuration
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✅ All tests passed! The bot setup looks good.")
        print("\nTo run the bot:")
        print("1. Make sure you've configured your bot token and YouTube URL")
        print("2. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("Run 'python setup.py' to fix common setup issues.")

if __name__ == "__main__":
    main()