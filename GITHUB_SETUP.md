# GitHub Authentication Setup

You're getting a permission error because git is using different credentials. Here's how to fix it:

## Option 1: Use Personal Access Token (Recommended)

### Step 1: Create Personal Access Token on GitHub

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `render-deploy`
4. Select scopes: Check `repo` (this gives full repository access)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Update Git Remote with Token

```bash
# Update remote URL with your token (replace YOUR_TOKEN with the actual token)
git remote set-url origin https://domdbeng:YOUR_TOKEN@github.com/domdbeng/YoutubeDownloader.git

# Now push
git push -u origin main
```

**Important**: Replace `YOUR_TOKEN` with the actual token you copied from GitHub.

## Option 2: Use GitHub CLI (Easiest)

### Install GitHub CLI

```bash
# macOS
brew install gh

# Or download from: https://cli.github.com/
```

### Login to GitHub

```bash
# Authenticate with your new GitHub account
gh auth login

# Follow the prompts:
# - Choose GitHub.com
# - Choose HTTPS
# - Authenticate in browser
# - Select your account (domdbeng)
```

### Push to GitHub

```bash
# Push using GitHub CLI
git push -u origin main
```

## Option 3: Update Git Credentials

### Clear old credentials

```bash
# macOS - Remove old credentials from Keychain
git credential-osxkeychain erase
host=github.com
protocol=https
[Press Enter twice]

# Or use credential helper
git config --global credential.helper osxkeychain
```

### Push again (will prompt for credentials)

```bash
git push -u origin main
```

When prompted:
- Username: `domdbeng`
- Password: Use your Personal Access Token (not your GitHub password)

## Option 4: Use SSH (Alternative)

### Generate SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519
```

### Add SSH Key to GitHub

1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Go to https://github.com/settings/keys
3. Click "New SSH key"
4. Paste your public key
5. Click "Add SSH key"

### Update Remote to Use SSH

```bash
# Change remote URL to SSH
git remote set-url origin git@github.com:domdbeng/YoutubeDownloader.git

# Push
git push -u origin main
```

## Quick Fix: Personal Access Token

**Fastest method:**

1. Create token: https://github.com/settings/tokens (classic token with `repo` scope)
2. Update remote:
   ```bash
   git remote set-url origin https://domdbeng:YOUR_TOKEN@github.com/domdbeng/YoutubeDownloader.git
   ```
3. Push:
   ```bash
   git push -u origin main
   ```

## After Pushing

Once your code is on GitHub, you can deploy to Render:

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub account (domdbeng)
4. Select `YoutubeDownloader` repository
5. Configure and deploy!

## Troubleshooting

### Still Getting 403 Error?
- Make sure you're using the correct token
- Verify the token has `repo` scope
- Check that your GitHub username is correct (domdbeng)

### Token Not Working?
- Generate a new token
- Make sure it has the `repo` scope
- Try using SSH instead

