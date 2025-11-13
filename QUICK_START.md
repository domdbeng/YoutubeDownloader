# Quick Start: Deploy to Render

## ✅ What's Done
- ✅ Git repository initialized
- ✅ All files committed
- ✅ Dockerfile configured with FFmpeg
- ✅ Gunicorn configured for production
- ✅ Render configuration files created

## 🚀 Next Steps

### 1. Push to GitHub

**Option A: Create new repository on GitHub**
1. Go to https://github.com/new
2. Create repository (e.g., `youtube-downloader`)
3. **DO NOT** initialize with README, .gitignore, or license
4. Copy the repository URL
5. Run these commands:

```bash
# Add GitHub remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Option B: If you already have a GitHub repository**
```bash
# Add your existing repository
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Deploy to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Sign up or Log in** (free account)
3. **Click "New +"** → **"Web Service"**
4. **Connect GitHub** (if not already connected)
5. **Select your repository**
6. **Configure**:
   - **Name**: `youtube-downloader` (or your preferred name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Docker Context**: `.`
7. **Plan**: Select `Free`
8. **Click "Create Web Service"**

### 3. Wait for Build
- First build takes 5-10 minutes
- Render will install FFmpeg and dependencies
- Check build logs for any issues

### 4. Access Your App
- Render will provide a URL like: `https://youtube-downloader.onrender.com`
- Your app is live! 🎉

## 📝 Important Notes

### Free Tier Limitations
- **Memory**: 512MB (large videos may fail)
- **Storage**: Ephemeral (files deleted on restart)
- **Spin-down**: Service sleeps after 15 min inactivity
- **Cold start**: First request after spin-down takes ~30 seconds

### Troubleshooting

**Build fails?**
- Check build logs in Render dashboard
- Ensure all files are committed and pushed
- Verify Dockerfile syntax

**App crashes?**
- Check logs in Render dashboard
- Verify PORT is set correctly
- Check memory usage (may need to limit video quality)

**Service spins down?**
- This is normal for free tier
- First request after inactivity takes ~30 seconds
- Consider upgrading for always-on service

## 🔄 Updating Your App

After making changes:
```bash
git add .
git commit -m "Your changes"
git push
```

Render will automatically detect and redeploy.

## 📚 More Information

- See `DEPLOY.md` for detailed deployment guide
- See `HOSTING_GUIDE.md` for hosting options
- See `README.md` for app documentation

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Check build logs in Render dashboard

