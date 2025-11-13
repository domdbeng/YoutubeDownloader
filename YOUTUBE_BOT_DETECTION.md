# YouTube Bot Detection - Solutions

## Issue
YouTube sometimes requires verification ("Sign in to confirm you're not a bot") when it detects automated access.

## Solutions Implemented

### 1. Browser-like Headers
- User agent that mimics Chrome browser
- Proper HTTP headers (Accept, Accept-Language, etc.)
- Referer header set to YouTube
- Security headers (DNT, Upgrade-Insecure-Requests, etc.)

### 2. Android Client
- Using Android client (`player_client: ['android']`) which often works better than web client
- Android client is less likely to trigger bot detection

### 3. Retry Logic
- Increased retries (10 retries for downloads)
- Fragment retries for video fragments
- File access retries

### 4. Delays Between Requests
- Sleep interval between requests (1-3 seconds)
- Random delays to appear more human-like

### 5. Error Handling
- Better error messages for users
- Graceful handling of bot detection errors

## If Issues Persist

### Option 1: Wait and Retry
- YouTube often blocks temporarily
- Wait a few minutes and try again
- The block may clear automatically

### Option 2: Update yt-dlp
```bash
pip install --upgrade yt-dlp
```
- Latest versions often have fixes for bot detection
- Current version: >=2024.12.13

### Option 3: Use Cookies (Advanced)
If the issue persists, you can use cookies from your browser:

1. **Export cookies from browser:**
   - Use a browser extension like "Get cookies.txt LOCALLY"
   - Or use yt-dlp's cookie export feature

2. **Add cookies to yt-dlp:**
   ```python
   ydl_opts = {
       'cookies': '/path/to/cookies.txt',
       # ... other options
   }
   ```

3. **Update app.py:**
   - Add cookie file support
   - Store cookies securely
   - Refresh cookies periodically

**Note**: Cookies require:
- User to export cookies from their browser
- Cookies expire and need refreshing
- More complex implementation
- Not ideal for public web service

### Option 4: Use Proxy/VPN
- Use rotating proxies
- More complex setup
- May violate YouTube's Terms of Service

### Option 5: Rate Limiting
- Add delays between requests
- Limit concurrent downloads
- Implement request throttling

## Current Implementation

The app now includes:
- ✅ Browser-like headers
- ✅ Android client
- ✅ Retry logic
- ✅ Delays between requests
- ✅ Better error handling
- ✅ User-friendly error messages

## Testing

1. Try downloading a video
2. If you get bot detection error:
   - Wait a few minutes
   - Try again
   - Error should clear

## Monitoring

- Check error logs in Render dashboard
- Monitor bot detection errors
- Track success rate
- Adjust delays if needed

## Future Improvements

1. **Cookie Support (if needed):**
   - Add cookie file upload
   - Store cookies securely
   - Auto-refresh cookies

2. **Rate Limiting:**
   - Implement request throttling
   - Limit concurrent downloads
   - Queue system

3. **Proxy Support:**
   - Rotating proxies
   - Better IP rotation
   - More reliable access

4. **User Agent Rotation:**
   - Rotate user agents
   - Use different browsers
   - More realistic requests

## Notes

- YouTube's bot detection is constantly evolving
- Solutions may need updates over time
- Some videos may require authentication
- Rate limiting helps avoid detection
- Android client is more reliable than web client

## Resources

- yt-dlp GitHub: https://github.com/yt-dlp/yt-dlp
- yt-dlp FAQ: https://github.com/yt-dlp/yt-dlp/wiki/FAQ
- Cookie Export: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies

