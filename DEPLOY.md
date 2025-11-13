# Deploy to Render - Step by Step Guide

## Prerequisites
1. GitHub account
2. Render account (sign up at https://render.com)

## Step 1: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: YouTube downloader Flask app"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `youtube-downloader`)
3. **DO NOT** initialize with README, .gitignore, or license
4. Copy the repository URL

## Step 3: Push to GitHub

```bash
# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/youtube-downloader.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub account** (if not already connected)
4. **Select your repository** (`youtube-downloader`)
5. **Configure the service**:
   - **Name**: `youtube-downloader` (or any name you prefer)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `./` if required)
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile` (or `./Dockerfile`)
   - **Docker Context**: `.` (current directory)
6. **Environment Variables** (optional, already set in render.yaml):
   - `PORT`: `5000` (Render sets this automatically)
   - `FLASK_DEBUG`: `False`
7. **Plan**: Select `Free` plan
8. **Click "Create Web Service"**

## Step 5: Wait for Deployment

- Render will build your Docker image (this takes 5-10 minutes)
- The build process will:
  1. Install FFmpeg
  2. Install Python dependencies
  3. Build the Docker image
  4. Start the service

## Step 6: Access Your App

- Once deployed, Render will provide a URL like: `https://youtube-downloader.onrender.com`
- Your app should be accessible at this URL

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure Dockerfile is correct
- Verify requirements.txt has all dependencies

### App Crashes
- Check logs in Render dashboard
- Verify PORT environment variable is set
- Check if FFmpeg is installed correctly

### Long Build Time
- First build takes longer (downloading Docker images)
- Subsequent builds are faster (cached layers)

### Service Spins Down
- Free tier services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to start
- Consider upgrading to paid plan for always-on service

## Updating Your App

1. Make changes to your code
2. Commit changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```
3. Render will automatically detect changes and redeploy

## Environment Variables (Optional)

You can set additional environment variables in Render dashboard:
- `FLASK_DEBUG`: Set to `False` for production
- `CLEANUP_INTERVAL`: Override cleanup interval (default: 300 seconds)
- `FILE_MAX_AGE`: Override file max age (default: 3600 seconds)

## Free Tier Limitations

- **Memory**: 512MB RAM
- **CPU**: Shared CPU
- **Storage**: Ephemeral (files are lost on restart)
- **Bandwidth**: Unlimited (but be mindful)
- **Spin-down**: Service spins down after 15 minutes of inactivity
- **Build time**: Limited build minutes per month

## Notes

- Files are stored temporarily (ephemeral storage)
- Large videos may cause memory issues (512MB limit)
- Service may restart occasionally (free tier)
- Consider upgrading for production use

## Support

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Render Community: https://community.render.com

