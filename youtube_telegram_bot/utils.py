"""
Utility functions for the YouTube Live Frame Capture Telegram Bot
"""

import os
import logging
from typing import List

logger = logging.getLogger(__name__)

def validate_youtube_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid YouTube URL
    
    Args:
        url (str): YouTube URL to validate
        
    Returns:
        bool: True if valid YouTube URL, False otherwise
    """
    valid_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc in valid_domains
    except Exception as e:
        logger.warning(f"URL validation error: {e}")
        return False

def cleanup_temp_directory(temp_dir: str, max_age_hours: int = 24) -> None:
    """
    Clean up old temporary files in the temp directory
    
    Args:
        temp_dir (str): Path to temporary directory
        max_age_hours (int): Maximum age of files to keep (in hours)
    """
    import time
    
    if not os.path.exists(temp_dir):
        return
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    try:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    logger.info(f"Cleaned up old temp file: {filename}")
    except Exception as e:
        logger.warning(f"Error during temp directory cleanup: {e}")

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.1f} GB"

def is_ffmpeg_available() -> bool:
    """
    Check if ffmpeg is available in the system PATH
    
    Returns:
        bool: True if ffmpeg is available, False otherwise
    """
    import subprocess
    
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_system_info() -> dict:
    """
    Get basic system information for debugging
    
    Returns:
        dict: System information
    """
    import platform
    import sys
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': sys.version,
        'ffmpeg_available': is_ffmpeg_available()
    }