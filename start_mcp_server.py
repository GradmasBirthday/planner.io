#!/usr/bin/env python3
"""
Startup script for Travel Planning MCP Server

This script initializes and starts the MCP server with travel planning tools.
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from planner.mcp_config import get_mcp_config, validate_configuration, create_sample_env_file
from planner.mcp_server import TravelPlanningMCPServer

def setup_logging(config):
    """Setup logging configuration"""
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if enabled
    if config.enable_file_logging:
        try:
            log_file_path = config.get_log_file_path()
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            print(f"Logging to file: {log_file_path}")
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")

def check_environment():
    """Check if .env file exists and create example if needed"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("No .env file found.")
        if not env_example.exists():
            print("Creating .env.example file...")
            create_sample_env_file(".env.example")
        
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your actual API keys")
        print("3. Run this script again")
        return False
    
    return True

async def main():
    """Main function to start the MCP server"""
    print("Starting Travel Planning MCP Server...")
    
    # Check environment setup
    if not check_environment():
        sys.exit(1)
    
    # Load configuration
    try:
        config = get_mcp_config()
        print(f"Loaded configuration for {config.server_name} v{config.server_version}")
    except Exception as e:
        print(f"[ERROR] Error loading configuration: {e}")
        sys.exit(1)
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    # Validate configuration
    print("[VALIDATING] Validating configuration...")
    validation_status = validate_configuration()
    
    if not validation_status["valid"]:
        print("[ERROR] Configuration validation failed:")
        for error in validation_status["errors"]:
            print(f"   - {error}")
        sys.exit(1)
    
    if validation_status["warnings"]:
        print("[WARNING]  Configuration warnings:")
        for warning in validation_status["warnings"]:
            print(f"   - {warning}")
    
    print("[OK] Configuration validation passed")
    
    # Print configuration summary
    print("\n[CONFIG] Configuration Summary:")
    for key, value in validation_status["config_summary"].items():
        print(f"   {key}: {value}")
    
    # Initialize and start server
    try:
        print(f"\n[INIT]  Initializing MCP server...")
        server = TravelPlanningMCPServer()
        
        print("Available tools:")
        tools = server.server.list_tools()
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        print(f"\n[STARTING] Starting server in {'PRODUCTION' if config.is_production() else 'MOCK'} mode...")
        logger.info(f"Starting {config.server_name} v{config.server_version}")
        
        # Start the server
        await server.run()
        
    except KeyboardInterrupt:
        print("\n[STOPPED] Server stopped by user")
        logger.info("Server stopped by user interrupt")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

def print_help():
    """Print help information"""
    help_text = """
Travel Planning MCP Server

This server provides AI-powered travel planning tools that can be used with
Google's Gemini AI through the Model Context Protocol (MCP).

SETUP:
1. Install dependencies: pip install -r requirements.txt
2. Copy .env.example to .env
3. Update .env with your API keys (at minimum GOOGLE_API_KEY)
4. Run: python start_mcp_server.py

AVAILABLE TOOLS:
- create_travel_plan - Create comprehensive travel plans
- search_travel_products - Find travel gear and products
- discover_local_experiences - Find local attractions and events
- coordinate_bookings - Help with reservations and bookings
- execute_agent_task - Run specific agent tasks

ENVIRONMENT VARIABLES:
- GOOGLE_API_KEY - Required for production mode
- ENABLE_MOCK_MODE - Set to false for production
- LOG_LEVEL - DEBUG, INFO, WARNING, ERROR
- See .env.example for full configuration options

For more information, see the documentation.
"""
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        print_help()
    else:
        # Check Python version
        if sys.version_info < (3, 8):
            print("[ERROR] Python 3.8 or higher is required")
            sys.exit(1)
        
        # Run the server
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            sys.exit(1)