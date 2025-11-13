# YouTube Downloader Web App

A Flask web application for downloading YouTube videos and playlists as MP3 audio or MP4 video files.

## Features

- 📥 Download single videos or entire playlists
- 🎵 Audio-only downloads (MP3)
- 🎬 Video downloads (MP4)
- 👀 Preview videos before downloading
- 🗑️ Automatic file cleanup
- 🎨 Modern, responsive UI

## Requirements

- Python 3.12+
- FFmpeg (for audio/video processing)
- Flask
- yt-dlp

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/

5. Run the application:
```bash
python app.py
```

6. Open your browser to `http://localhost:5000`

## Deployment

See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for free hosting options and deployment instructions.

### Quick Deploy to Render

1. Push your code to GitHub
2. Create an account on [Render](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Use the Dockerfile for deployment
6. Add environment variable: `PORT=5000`
7. Deploy!

## Usage

1. Enter a YouTube URL (video or playlist)
2. Choose between single video or playlist
3. Select audio-only (MP3) or video (MP4)
4. Click "Preview Video" to see the content
5. Click "Download" to start the download
6. Download files individually when ready

## File Cleanup

- Files are automatically deleted after download
- Files are cleaned up after 1 hour if not downloaded
- Files are cleaned up after 30 minutes of inactivity
- Automatic cleanup runs every 5 minutes

## License

MIT License

## Disclaimer

This tool is for personal use only. Respect YouTube's Terms of Service and copyright laws. Only download content you have permission to download.

