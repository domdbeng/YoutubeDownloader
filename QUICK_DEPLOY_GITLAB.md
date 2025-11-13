# Quick Deploy to Render via GitLab

## Step 1: Create GitLab Account & Repository

1. Go to https://gitlab.com and sign up (free)
2. Click "New project" → "Create blank project"
3. Project name: `youtube-downloader`
4. Visibility: **Private** (or Public)
5. **DO NOT** check "Initialize repository with a README"
6. Click "Create project"

## Step 2: Push Your Code to GitLab

Run these commands in your project directory:

```bash
# Add GitLab as remote (replace YOUR_USERNAME with your GitLab username)
git remote add origin https://gitlab.com/YOUR_USERNAME/youtube-downloader.git

# Rename branch to main (if not already)
git branch -M main

# Push to GitLab
git push -u origin main
```

**If you get authentication errors**, you'll need to create a Personal Access Token:

1. Go to GitLab → Settings → Access Tokens
2. Token name: `render-deploy`
3. Scopes: Check `write_repository`
4. Click "Create personal access token"
5. Copy the token
6. Use it as password when pushing, or update remote URL:

```bash
# Use token in remote URL (replace YOUR_TOKEN with your actual token)
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@gitlab.com/YOUR_USERNAME/youtube-downloader.git
git push -u origin main
```

## Step 3: Deploy to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Sign up or Log in** (free account)
3. **Click "New +"** → **"Web Service"**
4. **Connect GitLab**:
   - Click "Connect account"
   - Select "GitLab"
   - Authorize Render to access your GitLab account
5. **Select your repository**: `youtube-downloader`
6. **Configure the service**:
   - **Name**: `youtube-downloader`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Docker Context**: `.`
7. **Plan**: Select `Free`
8. **Click "Create Web Service"**

## Step 4: Wait for Deployment

- First build takes 5-10 minutes
- Render will:
  1. Clone your GitLab repository
  2. Build Docker image
  3. Install FFmpeg and dependencies
  4. Start your app

## Step 5: Access Your App

- Once deployed, Render provides a URL like:
  `https://youtube-downloader.onrender.com`
- Your app is live! 🎉

## Troubleshooting

### Authentication Error
- Create GitLab Personal Access Token
- Use token in git remote URL or as password

### Build Fails
- Check build logs in Render dashboard
- Verify Dockerfile is correct
- Ensure all files are pushed to GitLab

### Push Error
- Make sure you're using HTTPS URL
- Verify your GitLab username is correct
- Try using Personal Access Token

## That's It!

Your app should now be deployed on Render via GitLab. Any future changes:

```bash
git add .
git commit -m "Your changes"
git push
```

Render will automatically detect and redeploy!

