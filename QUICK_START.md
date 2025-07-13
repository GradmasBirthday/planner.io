# Quick Start: Deploy to Fly.io

## 🚀 One-Command Deployment

1. **Install Fly CLI** (if not already installed):
   ```powershell
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login to Fly.io**:
   ```powershell
   fly auth login
   ```

3. **Run the deployment script**:
   ```powershell
   .\deploy.ps1
   ```

## 📋 Manual Steps (if script doesn't work)

### 1. Initialize App
```powershell
fly launch
# Choose app name: tripmaxxing-planner
# Choose region: iad (US East)
# Deploy now: No
```

### 2. Set Environment Variables
```powershell
fly secrets set GOOGLE_API_KEY="your_google_api_key_here"
```

### 3. Deploy
```powershell
fly deploy
```

### 4. Verify
```powershell
fly status
fly open
```

## 🔧 Configuration Files Created

- **`fly.toml`** - Fly.io app configuration
- **`Dockerfile`** - Container configuration
- **`.dockerignore`** - Excludes unnecessary files
- **`deploy.ps1`** - Automated deployment script
- **`DEPLOYMENT.md`** - Detailed deployment guide

## 🌐 Your App Will Be Available At

```
https://tripmaxxing-planner.fly.dev
```

## 📡 API Endpoints

- **Health Check**: `GET /health`
- **API Info**: `GET /`
- **Chat**: `POST /chat`
- **Travel Planning**: `POST /api/v1/travel/plan`
- **Local Discovery**: `POST /api/v1/local/discover`

## 💰 Cost Optimization

- **Auto-stop**: Machines stop when not in use
- **Min machines**: 0 (no cost when idle)
- **Shared CPU**: Cost-effective for development

## 🆘 Troubleshooting

### Common Issues:

1. **"Fly CLI not found"**
   - Run: `iwr https://fly.io/install.ps1 -useb | iex`

2. **"Not authenticated"**
   - Run: `fly auth login`

3. **"App won't start"**
   - Check: `fly logs`
   - Verify: `fly secrets list`

4. **"Health check failing"**
   - Ensure GOOGLE_API_KEY is set
   - Check the `/health` endpoint returns 200

### Useful Commands:

```powershell
# View logs
fly logs

# Check status
fly status

# Scale app
fly scale count 2

# Update secrets
fly secrets set GOOGLE_API_KEY="new_key"

# Redeploy
fly deploy
```

## 📞 Support

- **Fly.io Docs**: https://fly.io/docs/
- **App Dashboard**: https://fly.io/apps/tripmaxxing-planner
- **Community**: https://community.fly.io/ 