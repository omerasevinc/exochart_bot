# YouTube Live Frame Capture Telegram Bot

A Telegram bot that captures and sends live video frames from YouTube streams on command.

## Features

- 📸 Capture live frames from YouTube streams
- 🤖 Simple Telegram bot interface
- ⚡ Fast response (10-30 seconds)
- 🔒 User authorization support
- 🧹 Automatic cleanup of temporary files
- 📱 Cross-platform support (Linux/Windows/macOS)

## Prerequisites

- Python 3.7+
- ffmpeg (system-level installation)
- Telegram Bot Token
- YouTube Live Stream URL

## Installation

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 2. Clone and Setup

```bash
# Navigate to project directory
cd youtube_telegram_bot

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` file with your values:
   - Get Telegram bot token from [@BotFather](https://t.me/botfather)
   - Set your YouTube live stream URL
   - Optionally set allowed user IDs

Or alternatively, edit `config.py` directly with your values.

## Usage

### 1. Start the Bot

```bash
python main.py
```

### 2. Telegram Commands

- Send `/start` to see welcome message
- Send `/help` for help information
- Send `btc`, `capture`, or `frame` to capture a frame

### 3. Example Interaction

```
User: btc
Bot: 📸 Capturing frame from live stream...
Bot: [sends captured image] 📸 Live stream frame captured!
```

## Configuration Options

Edit `config.py` to customize:

- `TRIGGER_COMMANDS`: Commands that trigger frame capture
- `FFMPEG_OPTIONS`: Video quality and resolution settings
- `TIMEOUT` values: Adjust for your network conditions
- `IMAGE_FORMAT`: Output image format (jpg/png)

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check bot token validity
   - Verify network connectivity
   - Check logs for error messages

2. **yt-dlp errors**
   - Verify YouTube URL is correct
   - Check if stream is live
   - Update yt-dlp: `pip install --upgrade yt-dlp`

3. **ffmpeg errors**
   - Ensure ffmpeg is installed and in PATH
   - Check ffmpeg version: `ffmpeg -version`
   - Verify stream format compatibility

4. **Permission errors**
   - Check write permissions in `temp_frames/` directory
   - Ensure sufficient disk space

5. **Timeout errors**
   - Increase timeout values in `config.py`
   - Check network speed and stability

### Debug Mode

Enable debug logging by modifying `main.py`:

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change from INFO to DEBUG
)
```

## Project Structure

```
youtube_telegram_bot/
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── bot_handler.py       # Telegram bot logic
├── frame_capture.py     # Frame capture engine
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env.template        # Environment variables template
├── README.md           # This file
└── temp_frames/        # Temporary frame storage
```

## Security Notes

- Keep your bot token secure and never commit it to version control
- Use environment variables for sensitive configuration
- Restrict bot access using `ALLOWED_USER_IDS` if needed
- Regularly update dependencies for security patches

## Performance Tips

- For high-frequency usage, consider implementing rate limiting
- Monitor disk space in `temp_frames/` directory
- Adjust image quality settings for balance between size and quality
- Use SSD storage for better I/O performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and personal use.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs for error details
3. Ensure all dependencies are correctly installed
4. Verify configuration settings