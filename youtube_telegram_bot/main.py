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