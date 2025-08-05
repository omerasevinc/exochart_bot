FROM python:3.11-slim

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY youtube_telegram_bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY youtube_telegram_bot/ .

# Create temp directory
RUN mkdir -p temp_frames

# Verify FFmpeg installation
RUN ffmpeg -version

# Run the bot
CMD ["python", "main.py"] 