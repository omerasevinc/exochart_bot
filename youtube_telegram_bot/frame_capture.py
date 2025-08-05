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