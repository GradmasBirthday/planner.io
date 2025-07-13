#!/usr/bin/env pwsh
# Fly.io Deployment Script for TripMaxxing Planner

Write-Host "🚀 Starting Fly.io deployment for TripMaxxing Planner..." -ForegroundColor Green

# Check if fly CLI is installed
try {
    $flyVersion = fly version
    Write-Host "✅ Fly CLI found: $flyVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Fly CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    exit 1
}

# Check if user is authenticated
try {
    $auth = fly auth whoami
    Write-Host "✅ Authenticated as: $auth" -ForegroundColor Green
} catch {
    Write-Host "❌ Not authenticated. Please run: fly auth login" -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Make sure to set GOOGLE_API_KEY" -ForegroundColor Yellow
}

# Check if fly.toml exists
if (Test-Path "fly.toml") {
    Write-Host "✅ fly.toml configuration found" -ForegroundColor Green
} else {
    Write-Host "❌ fly.toml not found. Please run: fly launch" -ForegroundColor Red
    exit 1
}

# Check if Dockerfile exists
if (Test-Path "Dockerfile") {
    Write-Host "✅ Dockerfile found" -ForegroundColor Green
} else {
    Write-Host "❌ Dockerfile not found" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Pre-deployment checks completed" -ForegroundColor Cyan

# Ask user if they want to proceed
$proceed = Read-Host "`nDo you want to proceed with deployment? (y/N)"
if ($proceed -ne "y" -and $proceed -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Deploy the application
Write-Host "`n🚀 Deploying to Fly.io..." -ForegroundColor Green
try {
    fly deploy
    Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Deployment failed. Check the logs above." -ForegroundColor Red
    exit 1
}

# Show app status
Write-Host "`n📊 Checking app status..." -ForegroundColor Cyan
fly status

# Show app URL
Write-Host "`n🌐 Your app is available at:" -ForegroundColor Green
$appName = (Get-Content "fly.toml" | Select-String "app = " | ForEach-Object { $_.ToString().Split('"')[1] })
if ($appName) {
    Write-Host "   https://$appName.fly.dev" -ForegroundColor Cyan
} else {
    Write-Host "   Check fly status for the URL" -ForegroundColor Yellow
}

Write-Host "`n📝 Next steps:" -ForegroundColor Green
Write-Host "   1. Test the health endpoint: https://$appName.fly.dev/health" -ForegroundColor White
Write-Host "   2. Set environment variables: fly secrets set GOOGLE_API_KEY='your_key'" -ForegroundColor White
Write-Host "   3. View logs: fly logs" -ForegroundColor White
Write-Host "   4. Open app: fly open" -ForegroundColor White

Write-Host "`n🎉 Deployment script completed!" -ForegroundColor Green 