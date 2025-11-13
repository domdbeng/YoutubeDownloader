import os
import json
import threading
import time
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, Response
from yt_dlp import YoutubeDL
import shutil
from pathlib import Path
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

OUTPUT_FOLDER = "Downloaded_MP3s"
VIDEO_OUTPUT_FOLDER = "Downloaded_Videos"

# Ensure output folders exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(VIDEO_OUTPUT_FOLDER, exist_ok=True)

# Store download status, errors, and file paths
download_status = {}

# Cleanup configuration
CLEANUP_INTERVAL = 300  # Check every 5 minutes
FILE_MAX_AGE = 3600  # Delete files older than 1 hour (3600 seconds)


def get_video_info(url):
    """Extract video/playlist information without downloading"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Check if it's a playlist
            if 'entries' in info:
                # It's a playlist
                entries = list(info['entries'])
                playlist_info = {
                    'type': 'playlist',
                    'title': info.get('title', 'Untitled Playlist'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'video_count': len(entries),
                    'videos': []
                }
                
                for entry in entries[:10]:  # Limit to first 10 for preview
                    if entry:
                        video_id = entry.get('id', '')
                        playlist_info['videos'].append({
                            'title': entry.get('title', 'Unknown'),
                            'id': video_id,
                            'thumbnail': entry.get('thumbnail', ''),
                            'duration': entry.get('duration', 0),
                            'url': f"https://www.youtube.com/watch?v={video_id}"
                        })
                
                return playlist_info
            else:
                # It's a single video
                video_id = info.get('id', '')
                return {
                    'type': 'video',
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'id': video_id,
                    'url': f"https://www.youtube.com/watch?v={video_id}"
                }
    except Exception as e:
        return {'error': str(e)}


def download_media(url, media_type, format_type, download_id):
    """Download video or playlist in background"""
    current_time = time.time()
    download_status[download_id] = {
        'status': 'processing', 
        'error': None, 
        'files': [], 
        'folder': None,
        'created_at': current_time,
        'last_accessed': current_time
    }
    try:
        # Create a temporary directory for this download
        if format_type == 'audio':
            base_folder = OUTPUT_FOLDER
        else:
            base_folder = VIDEO_OUTPUT_FOLDER
        
        temp_folder = os.path.join(base_folder, download_id)
        os.makedirs(temp_folder, exist_ok=True)
        
        if media_type == 'playlist':
            if format_type == 'audio':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(temp_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True,
                }
            else:  # video
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
                    'outtmpl': os.path.join(temp_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'quiet': True,
                }
        else:  # single video
            if format_type == 'audio':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(temp_folder, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True,
                }
            else:  # video
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
                    'outtmpl': os.path.join(temp_folder, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'quiet': True,
                }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Wait a moment to ensure all files are written
        time.sleep(2)
        
        # Collect all downloaded files
        downloaded_files = []
        file_info = []
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    downloaded_files.append(file_path)
                    # Store relative path for serving
                    rel_path = os.path.relpath(file_path, temp_folder)
                    file_info.append({
                        'name': file,
                        'path': rel_path,
                        'size': os.path.getsize(file_path)
                    })
        
        if not downloaded_files:
            error_msg = 'No files were downloaded'
            download_status[download_id] = {'status': 'error', 'error': error_msg, 'files': [], 'folder': None}
            # Clean up empty folder
            shutil.rmtree(temp_folder, ignore_errors=True)
            return {'status': 'error', 'message': error_msg}
        
        # Store file information in download status
        folder_type = 'audio' if format_type == 'audio' else 'video'
        download_status[download_id] = {
            'status': 'complete',
            'error': None,
            'files': file_info,
            'folder': folder_type,
            'media_type': media_type,
            'created_at': current_time,
            'last_accessed': current_time
        }
        
        return {'status': 'success', 'files': file_info}
    except Exception as e:
        error_msg = str(e)
        download_status[download_id] = {'status': 'error', 'error': error_msg, 'files': [], 'folder': None}
        # Clean up on error
        try:
            if 'temp_folder' in locals():
                shutil.rmtree(temp_folder, ignore_errors=True)
        except:
            pass
        return {'status': 'error', 'message': error_msg}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/preview', methods=['POST'])
def preview():
    """Get video/playlist information for preview"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    info = get_video_info(url)
    
    if 'error' in info:
        return jsonify(info), 400
    
    return jsonify(info)


@app.route('/download', methods=['POST'])
def download():
    """Start download process"""
    data = request.json
    url = data.get('url', '')
    media_type = data.get('media_type', 'video')  # 'video' or 'playlist'
    format_type = data.get('format_type', 'audio')  # 'audio' or 'video'
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    download_id = str(uuid.uuid4())
    
    # Start download in background thread
    thread = threading.Thread(
        target=download_media,
        args=(url, media_type, format_type, download_id)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'download_id': download_id, 'status': 'started'})


@app.route('/check_download/<download_id>')
def check_download(download_id):
    """Check if download is complete"""
    # Update last accessed time
    current_time = time.time()
    if download_id in download_status:
        download_status[download_id]['last_accessed'] = current_time
    
    # Check for errors first
    if download_id in download_status:
        status_info = download_status[download_id]
        if status_info['status'] == 'error':
            return jsonify({'status': 'error', 'error': status_info['error']})
        elif status_info['status'] == 'complete':
            return jsonify({
                'status': 'complete',
                'files': status_info['files'],
                'folder': status_info['folder'],
                'media_type': status_info.get('media_type', 'video')
            })
    
    return jsonify({'status': 'processing'})


@app.route('/download_file/<download_id>/<folder>/<path:filepath>')
def download_file(download_id, folder, filepath):
    """Serve individual downloaded files and delete them after download"""
    # Update last accessed time
    current_time = time.time()
    if download_id in download_status:
        download_status[download_id]['last_accessed'] = current_time
    
    if folder == 'audio':
        base_folder = OUTPUT_FOLDER
    else:
        base_folder = VIDEO_OUTPUT_FOLDER
    
    # Construct the file path
    download_folder = os.path.join(base_folder, download_id)
    file_path = os.path.join(download_folder, filepath)
    
    # Security: prevent directory traversal
    real_path = os.path.realpath(file_path)
    real_base = os.path.realpath(download_folder)
    
    if not real_path.startswith(real_base):
        return jsonify({'error': 'Access denied'}), 403
    
    # Verify the file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # Get the filename for download
    filename = os.path.basename(file_path)
    
    try:
        def generate_and_cleanup():
            """Stream file content and cleanup after"""
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(8192)  # Read in 8KB chunks
                    if not chunk:
                        break
                    yield chunk
            
            # After file is fully sent, delete it
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    # Check if folder is empty and remove it if so
                    try:
                        if os.path.exists(download_folder) and not os.listdir(download_folder):
                            os.rmdir(download_folder)
                            # Remove from download_status if folder is deleted
                            if download_id in download_status:
                                del download_status[download_id]
                    except OSError:
                        pass  # Folder not empty or already deleted
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        
        # Create response with streaming
        response = Response(
            generate_and_cleanup(),
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/octet-stream'
            }
        )
        
        return response
    except Exception as e:
        return jsonify({'error': f'Error serving file: {str(e)}'}), 500


@app.route('/cleanup/<download_id>/<folder>')
def cleanup(download_id, folder):
    """Clean up downloaded files after they've been downloaded"""
    if folder == 'audio':
        base_folder = OUTPUT_FOLDER
    else:
        base_folder = VIDEO_OUTPUT_FOLDER
    
    temp_folder = os.path.join(base_folder, download_id)
    try:
        shutil.rmtree(temp_folder, ignore_errors=True)
        if download_id in download_status:
            del download_status[download_id]
        return jsonify({'status': 'cleaned'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def cleanup_old_files():
    """Periodically clean up old files that haven't been downloaded"""
    while True:
        try:
            current_time = time.time()
            folders_to_check = [
                (OUTPUT_FOLDER, 'audio'),
                (VIDEO_OUTPUT_FOLDER, 'video')
            ]
            
            # Clean up based on download_status
            download_ids_to_remove = []
            for download_id, status_info in list(download_status.items()):
                status = status_info.get('status')
                created_at = status_info.get('created_at', current_time)
                last_accessed = status_info.get('last_accessed', created_at)
                age = current_time - created_at
                time_since_access = current_time - last_accessed
                
                should_cleanup = False
                
                if status == 'complete':
                    # Delete completed downloads if older than max age OR not accessed for 30 minutes
                    if age > FILE_MAX_AGE or time_since_access > 1800:  # 30 minutes
                        should_cleanup = True
                elif status == 'error':
                    # Clean up errors after 10 minutes
                    if age > 600:  # 10 minutes
                        should_cleanup = True
                elif status == 'processing':
                    # Don't delete files that are still processing
                    continue
                
                if should_cleanup:
                    folder_type = status_info.get('folder', 'audio')
                    base_folder = OUTPUT_FOLDER if folder_type == 'audio' else VIDEO_OUTPUT_FOLDER
                    temp_folder = os.path.join(base_folder, download_id)
                    
                    try:
                        if os.path.exists(temp_folder):
                            shutil.rmtree(temp_folder, ignore_errors=True)
                            print(f"Cleaned up download {download_id} (status: {status}, age: {age:.0f}s)")
                        download_ids_to_remove.append(download_id)
                    except Exception as e:
                        print(f"Error cleaning up {download_id}: {e}")
            
            # Remove from download_status
            for download_id in download_ids_to_remove:
                if download_id in download_status:
                    del download_status[download_id]
            
            # Also scan folders for orphaned files (files not in download_status)
            for base_folder, folder_type in folders_to_check:
                if os.path.exists(base_folder):
                    for item in os.listdir(base_folder):
                        item_path = os.path.join(base_folder, item)
                        if os.path.isdir(item_path) and item not in download_status:
                            # Check if folder is old (older than max age based on folder creation time)
                            try:
                                folder_age = current_time - os.path.getctime(item_path)
                                if folder_age > FILE_MAX_AGE:
                                    shutil.rmtree(item_path, ignore_errors=True)
                                    print(f"Cleaned up orphaned folder: {item_path}")
                            except Exception as e:
                                print(f"Error cleaning up orphaned folder {item_path}: {e}")
        
        except Exception as e:
            print(f"Error in cleanup thread: {e}")
        
        # Wait before next cleanup
        time.sleep(CLEANUP_INTERVAL)


# Start cleanup thread when app starts
cleanup_thread = None
cleanup_thread_started = False

def start_cleanup_thread():
    """Start the background cleanup thread"""
    global cleanup_thread, cleanup_thread_started
    if not cleanup_thread_started:
        cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
        cleanup_thread.start()
        cleanup_thread_started = True

# Start cleanup thread when module is imported (for Gunicorn)
start_cleanup_thread()

if __name__ == '__main__':
    # Get port from environment variable (for hosting platforms)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=debug)

