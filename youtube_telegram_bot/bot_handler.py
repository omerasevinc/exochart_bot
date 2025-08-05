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