# Fly.io Deployment Guide for TripMaxxing Planner

## Prerequisites

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS
   curl -L https://fly.io/install.sh | sh
   
   # Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and login to Fly.io**
   ```bash
   fly auth signup
   # or if you already have an account:
   fly auth login
   ```

## Environment Variables Setup

Create a `.env` file in your project root (this will be used locally, not deployed):

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

## Deployment Steps

### 1. Initialize Fly App (First time only)

```bash
# Navigate to your project directory
cd planner.io

# Initialize the Fly app
fly launch
```

When prompted:
- **App name**: `tripmaxxing-planner` (or choose your own)
- **Region**: Choose the closest to your users (e.g., `iad` for US East)
- **Would you like to deploy now?**: `No` (we'll do this manually)

### 2. Set Environment Variables

```bash
# Set your Google API key
fly secrets set GOOGLE_API_KEY="your_actual_google_api_key_here"

# Set any other environment variables
fly secrets set NODE_ENV="production"
```

### 3. Create Volume (Optional - for data persistence)

```bash
# Create a volume for data storage
fly volumes create tripmaxxing_data --size 1 --region iad
```

### 4. Deploy the Application

```bash
# Deploy to Fly.io
fly deploy
```

### 5. Verify Deployment

```bash
# Check app status
fly status

# View logs
fly logs

# Open the app in browser
fly open
```

## Configuration Files

### fly.toml
- **App name**: `tripmaxxing-planner`
- **Primary region**: `iad` (US East)
- **Port**: 8000
- **Health checks**: Configured to check `/health` endpoint
- **Auto-scaling**: Enabled with min 0 machines (cost-effective)

### Dockerfile
- **Base image**: Python 3.12-slim
- **Dependencies**: Installs from both requirements files
- **Health check**: Monitors `/health` endpoint
- **Port**: Exposes 8000

## API Endpoints

Once deployed, your API will be available at:
- **Base URL**: `https://tripmaxxing-planner.fly.dev`
- **Health Check**: `GET /health`
- **API Info**: `GET /`
- **Chat**: `POST /chat`
- **Travel Planning**: `POST /api/v1/travel/plan`
- **Local Discovery**: `POST /api/v1/local/discover`

## Testing the Deployed API

```bash
# Health check
curl https://tripmaxxing-planner.fly.dev/health

# Chat test
curl -X POST https://tripmaxxing-planner.fly.dev/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I want to plan a trip to Tokyo"}'

# Travel planning
curl -X POST https://tripmaxxing-planner.fly.dev/api/v1/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "travel_dates": "2024-04-15 to 2024-04-22",
    "budget": "$3000",
    "travel_style": "cultural",
    "group_size": 2
  }'
```

## Monitoring and Management

### View Logs
```bash
fly logs
```

### Scale the App
```bash
# Scale to 2 instances
fly scale count 2

# Scale to 0 (pause when not in use)
fly scale count 0
```

### Update Environment Variables
```bash
fly secrets set GOOGLE_API_KEY="new_api_key"
```

### Redeploy
```bash
fly deploy
```

## Troubleshooting

### Common Issues

1. **Build fails**
   ```bash
   # Check build logs
   fly logs
   
   # Try building locally first
   docker build -t tripmaxxing-planner .
   ```

2. **App won't start**
   ```bash
   # Check app status
   fly status
   
   # View detailed logs
   fly logs --all
   ```

3. **Environment variables not set**
   ```bash
   # List current secrets
   fly secrets list
   
   # Set missing variables
   fly secrets set GOOGLE_API_KEY="your_key"
   ```

### Health Check Issues

If health checks are failing:
1. Ensure the `/health` endpoint returns `200 OK`
2. Check that the app is listening on port 8000
3. Verify environment variables are set correctly

## Cost Optimization

- **Auto-stop machines**: Enabled (machines stop when not in use)
- **Min machines**: 0 (no cost when idle)
- **Shared CPU**: Cost-effective for development
- **512MB RAM**: Sufficient for the application

## Security Notes

- **HTTPS**: Automatically enabled by Fly.io
- **Secrets**: Use `fly secrets` for sensitive data
- **Environment variables**: Never commit API keys to git

## Next Steps

1. **Connect frontend**: Update your frontend to use the deployed API URL
2. **Set up monitoring**: Configure alerts in Fly.io dashboard
3. **Custom domain**: Add a custom domain if needed
4. **CI/CD**: Set up automatic deployments from your git repository

## Support

- **Fly.io Docs**: https://fly.io/docs/
- **Fly.io Community**: https://community.fly.io/
- **App Dashboard**: https://fly.io/apps/tripmaxxing-planner 