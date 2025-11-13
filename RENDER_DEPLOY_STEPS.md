# Step-by-Step: Deploy to Render

## Prerequisites ✅
- ✅ Code is on GitHub: https://github.com/domdbeng/YoutubeDownloader
- ✅ All files are committed
- ✅ Dockerfile is ready
- ✅ Requirements.txt includes gunicorn

## Step 1: Go to Render Dashboard

1. **Open your browser**
2. **Go to**: https://dashboard.render.com
3. **Sign up** (if you don't have an account) or **Log in**
   - You can sign up with GitHub, Google, or email
   - Free account is available

## Step 2: Create New Web Service

1. **Click the "New +" button** (top right corner)
2. **Select "Web Service"** from the dropdown menu

## Step 3: Connect GitHub Account

1. **Click "Connect account"** or **"Connect GitHub"**
2. You'll be redirected to GitHub
3. **Authorize Render** to access your GitHub account
4. Make sure you're authorizing with the correct account (**domdbeng**)
5. **Click "Authorize render"** on GitHub
6. You'll be redirected back to Render

## Step 4: Select Your Repository

1. In the repository list, **find and click on**: `YoutubeDownloader`
2. Repository should show: `domdbeng/YoutubeDownloader`
3. **Click "Connect"** next to your repository

## Step 5: Configure Your Service

Fill in the following settings:

### Basic Settings:
- **Name**: `youtube-downloader` (or any name you like)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: Leave **empty** (or put `.` if required)

### Build & Deploy Settings:
- **Environment**: Select **`Docker`**
- **Dockerfile Path**: `Dockerfile`
- **Docker Context**: `.` (period/current directory)

### Advanced Settings (Optional):
- **Auto-Deploy**: `Yes` (automatically deploy when you push to GitHub)
- **Health Check Path**: `/` (leave default)

### Plan:
- **Plan**: Select **`Free`** (or upgrade if needed)

## Step 6: Environment Variables (Optional)

You can skip this - the app uses defaults, but you can set:

- **Key**: `PORT` → **Value**: `5000` (Render sets this automatically)
- **Key**: `FLASK_DEBUG` → **Value**: `False`

**Note**: These are already configured in `render.yaml`, so you can skip this step.

## Step 7: Create Web Service

1. **Review your settings**
2. **Click "Create Web Service"** button (bottom)
3. **Wait for deployment** (this takes 5-10 minutes)

## Step 8: Monitor Deployment

While waiting, you'll see:

1. **Build Logs**: Shows the build process
   - Installing FFmpeg
   - Installing Python dependencies
   - Building Docker image
   - Starting your app

2. **Build Status**: 
   - "Building" → "Deploying" → "Live"

3. **First Build Takes Longer**:
   - Downloading Docker images (~2-3 minutes)
   - Installing dependencies (~2-3 minutes)
   - Building application (~1-2 minutes)

## Step 9: Access Your App

Once deployment is complete:

1. **Render will provide a URL** like:
   - `https://youtube-downloader.onrender.com`
   - Or `https://youtube-downloader-xxxx.onrender.com`

2. **Click the URL** or copy it to your browser

3. **Your app should be live!** 🎉

## Step 10: Test Your App

1. **Open the URL** in your browser
2. **Try downloading a video**:
   - Enter a YouTube URL
   - Select audio or video
   - Click "Preview Video"
   - Click "Download"
3. **Verify everything works**

## Troubleshooting

### Build Fails?
- **Check build logs** in Render dashboard
- **Look for errors** in the logs
- **Verify Dockerfile** is correct
- **Check requirements.txt** has all dependencies

### App Crashes?
- **Check runtime logs** in Render dashboard
- **Look for error messages**
- **Verify PORT** is set correctly
- **Check memory usage** (free tier has 512MB limit)

### Service Spins Down?
- **Free tier** spins down after 15 minutes of inactivity
- **First request** after spin-down takes ~30 seconds
- **This is normal** for free tier

### Can't Find Repository?
- **Make sure** you connected the correct GitHub account
- **Check** your GitHub account is `domdbeng`
- **Verify** repository name is `YoutubeDownloader`

### Authentication Issues?
- **Reconnect GitHub** in Render dashboard
- **Check** GitHub permissions
- **Verify** you're using the correct account

## What Happens During Deployment

1. **Render clones** your GitHub repository
2. **Builds Docker image** using your Dockerfile
3. **Installs FFmpeg** (from Dockerfile)
4. **Installs Python dependencies** (from requirements.txt)
5. **Starts your app** with Gunicorn
6. **Provides a URL** for your app

## After Deployment

### Your App URL:
- Render provides a URL like: `https://youtube-downloader.onrender.com`
- You can customize it in Render settings (if needed)

### Update Your App:
1. **Make changes** to your code
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```
3. **Render automatically detects** and redeploys (if auto-deploy is enabled)

### Monitor Your App:
- **View logs** in Render dashboard
- **Check metrics** (CPU, memory, requests)
- **Monitor build history**

## Free Tier Limitations

- **Memory**: 512MB RAM (large videos may fail)
- **Storage**: Ephemeral (files deleted on restart)
- **Spin-down**: Service sleeps after 15 min inactivity
- **Cold start**: First request after spin-down takes ~30 seconds
- **Build time**: Limited build minutes per month

## Next Steps

1. ✅ Deploy to Render (follow steps above)
2. ✅ Test your app
3. ✅ Share the URL
4. ✅ Monitor usage
5. ✅ Consider upgrading for production use

## Support

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Render Community**: https://community.render.com
- **Check logs**: In Render dashboard → Logs tab

## Quick Reference

**Your Repository**: https://github.com/domdbeng/YoutubeDownloader

**Render Dashboard**: https://dashboard.render.com

**Steps**:
1. Go to Render
2. Click "New +" → "Web Service"
3. Connect GitHub
4. Select `YoutubeDownloader`
5. Configure: Docker, Dockerfile, Free plan
6. Click "Create Web Service"
7. Wait for deployment
8. Access your app!

---

**Ready to deploy? Follow the steps above!** 🚀

