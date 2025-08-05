#!/usr/bin/env python3
"""
Setup script for YouTube Live Frame Capture Telegram Bot
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg found: {version_line}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ FFmpeg not found")
    print("Please install FFmpeg:")
    print("  macOS: brew install ffmpeg")
    print("  Ubuntu/Debian: sudo apt install ffmpeg")
    print("  Windows: Download from https://ffmpeg.org/download.html")
    return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path('.env')
    template_file = Path('env_template.txt')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if template_file.exists():
        shutil.copy(template_file, env_file)
        print("📝 Created .env file from template")
        print("⚠️  Please edit .env file with your bot token and YouTube URL")
        return True
    else:
        print("❌ env_template.txt not found")
        return False

def create_temp_directory():
    """Create temp_frames directory"""
    temp_dir = Path('temp_frames')
    temp_dir.mkdir(exist_ok=True)
    print("✅ Created temp_frames directory")

def validate_config():
    """Basic configuration validation"""
    try:
        from config import Config
        config = Config()
        
        issues = []
        if config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            issues.append("TELEGRAM_BOT_TOKEN not set")
        
        if 'YOUR_LIVE_STREAM_ID' in config.YOUTUBE_LIVE_URL:
            issues.append("YOUTUBE_LIVE_URL not set")
        
        if issues:
            print("⚠️  Configuration issues found:")
            for issue in issues:
                print(f"   - {issue}")
            print("Please update config.py or .env file")
            return False
        
        print("✅ Configuration looks good")
        return True
        
    except ImportError as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 YouTube Live Frame Capture Telegram Bot Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check FFmpeg
    if not check_ffmpeg():
        success = False
    
    # Install dependencies
    if success and not install_dependencies():
        success = False
    
    # Create environment file
    create_env_file()
    
    # Create temp directory
    create_temp_directory()
    
    # Validate configuration
    validate_config()
    
    print("=" * 50)
    if success:
        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your bot token and YouTube URL")
        print("2. Run: python main.py")
        print("3. Test the bot by sending 'btc' to it on Telegram")
    else:
        print("❌ Setup completed with issues")
        print("Please resolve the issues above before running the bot")

if __name__ == "__main__":
    main()