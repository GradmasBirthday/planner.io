#!/usr/bin/env python3
"""
Startup script for Gemini API Proxy Server
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import google.generativeai
        import pydantic
        import dotenv
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_vars():
    """Check if required environment variables are set"""
    required_vars = ["GOOGLE_API_KEY"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"✗ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment")
        return False

    print("✓ All required environment variables are set")
    return True

def create_env_file():
    """Create a .env file template if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        template = """# API Keys (Required)
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"]
"""
        env_file.write_text(template)
        print("✓ Created .env file template")
        print("Please edit .env file with your API keys")
        return False
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Gemini API Proxy Server...")
    print("=" * 50)

    # Check if .env file exists
    if not create_env_file():
        sys.exit(1)

    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Warning: python-dotenv not installed, loading environment variables from system")

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Check environment variables
    if not check_env_vars():
        sys.exit(1)

    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    print(f"✓ Starting server at http://{host}:{port}")
    print(f"✓ Debug mode: {debug}")
    print(f"✓ API documentation: http://{host}:{port}/docs")
    print(f"✓ Health check: http://{host}:{port}/health")
    print("=" * 50)

    # Start the server
    try:
        import uvicorn
        uvicorn.run(
            "src.planner.gemini_server:app",
            host=host,
            port=port,
            reload=debug,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"✗ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 