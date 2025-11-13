# Deploy to Render Without GitHub

Since you can't use GitHub, here are alternative ways to deploy to Render:

## Option 1: Use GitLab (Recommended) ⭐

GitLab is free and works similarly to GitHub. Render supports GitLab!

### Step 1: Create GitLab Account
1. Go to https://gitlab.com
2. Sign up for a free account
3. Verify your email

### Step 2: Create GitLab Repository
1. Click "New project" → "Create blank project"
2. Name it (e.g., `youtube-downloader`)
3. **DO NOT** initialize with README
4. Set visibility to **Private** or **Public**
5. Click "Create project"

### Step 3: Push to GitLab
```bash
# Add GitLab remote (replace with your GitLab username and project name)
git remote add origin https://gitlab.com/YOUR_USERNAME/youtube-downloader.git

# Rename branch to main
git branch -M main

# Push to GitLab
git push -u origin main
```

### Step 4: Deploy to Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Click "Connect account" → Select **GitLab**
4. Authorize Render to access GitLab
5. Select your GitLab repository
6. Configure:
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Plan**: `Free`
7. Click "Create Web Service"

## Option 2: Use Bitbucket

Bitbucket is also free and supported by Render.

### Step 1: Create Bitbucket Account
1. Go to https://bitbucket.org
2. Sign up for a free account

### Step 2: Create Bitbucket Repository
1. Click "Create" → "Repository"
2. Name it (e.g., `youtube-downloader`)
3. **DO NOT** initialize with README
4. Click "Create repository"

### Step 3: Push to Bitbucket
```bash
# Add Bitbucket remote (replace with your Bitbucket username)
git remote add origin https://bitbucket.org/YOUR_USERNAME/youtube-downloader.git

# Rename branch to main
git branch -M main

# Push to Bitbucket
git push -u origin main
```

### Step 4: Deploy to Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Click "Connect account" → Select **Bitbucket**
4. Authorize Render
5. Select your Bitbucket repository
6. Configure as above

## Option 3: Use Render CLI (Direct Deployment)

Render CLI allows you to deploy directly from your local machine.

### Step 1: Install Render CLI
```bash
# macOS
brew install render

# Or using npm
npm install -g render-cli

# Or using pip
pip install render-cli
```

### Step 2: Login to Render
```bash
render login
```
This will open a browser to authenticate.

### Step 3: Create Render Blueprint
Create a `render.yaml` file (already exists) with:
```yaml
services:
  - type: web
    name: youtube-downloader
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    envVars:
      - key: PORT
        value: 5000
      - key: FLASK_DEBUG
        value: "False"
```

### Step 4: Deploy with CLI
```bash
# Deploy using render.yaml
render deploy

# Or create service directly
render services create web \
  --name youtube-downloader \
  --env docker \
  --dockerfilePath ./Dockerfile \
  --dockerContext .
```

**Note**: Render CLI may require the code to be in a Git repository (even local).

## Option 4: Use Public Git URL

If you have your code in any public Git repository (GitLab, Bitbucket, or even a self-hosted Git server):

### Step 1: Make Repository Public
Make sure your repository is publicly accessible.

### Step 2: Get Git URL
Get the HTTPS or SSH URL of your repository.

### Step 3: Deploy to Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Select "Public Git repository"
4. Enter your Git repository URL
5. Configure as above

## Option 5: Manual File Upload (Limited)

Unfortunately, Render doesn't support direct file upload for web services. However, you can:

### Alternative: Use Render's Manual Deploy (via Git)
1. Create a temporary Git repository on any Git provider (GitLab, Bitbucket)
2. Push your code there
3. Connect to Render
4. Once deployed, you can disconnect the Git integration if needed

## Quick Start: GitLab (Easiest Alternative)

Since GitLab is the most similar to GitHub, here's the quickest path:

### 1. Create GitLab Repository
```bash
# You already have git initialized and committed
# Just add GitLab remote and push
git remote add origin https://gitlab.com/YOUR_USERNAME/youtube-downloader.git
git branch -M main
git push -u origin main
```

### 2. Connect GitLab to Render
1. Go to Render dashboard
2. Connect GitLab account
3. Select repository
4. Deploy!

## Troubleshooting

### GitLab Push Issues
If you get authentication errors:
```bash
# Use personal access token
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@gitlab.com/YOUR_USERNAME/youtube-downloader.git
```

To create a GitLab token:
1. Go to GitLab → Settings → Access Tokens
2. Create token with `write_repository` scope
3. Use token as password when pushing

### Bitbucket Push Issues
Similar to GitLab, use app password:
1. Go to Bitbucket → Personal Settings → App Passwords
2. Create app password
3. Use it when pushing

### Render CLI Issues
```bash
# Check if logged in
render whoami

# List services
render services list

# Check logs
render logs <service-id>
```

## Recommended: GitLab

**Why GitLab?**
- ✅ Free and unlimited private repos
- ✅ Similar to GitHub interface
- ✅ Render supports it natively
- ✅ Easy to set up
- ✅ No credit card required

## Next Steps

1. **Choose a Git provider** (GitLab recommended)
2. **Create repository** on that provider
3. **Push your code** using git commands
4. **Connect to Render** using that provider
5. **Deploy!**

Your code is already committed and ready - you just need to push it to a Git provider that Render supports!

