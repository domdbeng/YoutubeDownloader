FROM python:3.12-slim

# Install FFmpeg and other dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories for downloads
RUN mkdir -p Downloaded_MP3s Downloaded_Videos

# Expose port
EXPOSE 5000

# Set environment variable
ENV PORT=5000

# Run the application with gunicorn
# Use --preload to start cleanup thread once, and --timeout for long video downloads
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 300 --preload app:app

