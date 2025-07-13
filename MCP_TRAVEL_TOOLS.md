# Travel Planning MCP Server & Gemini Tools

This repository contains a comprehensive Model Context Protocol (MCP) server that provides AI-powered travel planning tools for use with Google's Gemini AI and other compatible systems.

## 🌟 Features

### Available Tools

1. **create_travel_plan** - Create comprehensive travel plans with itineraries, recommendations, and booking information
2. **search_travel_products** - Find travel gear and products from Amazon and other platforms
3. **discover_local_experiences** - Discover local attractions, events, restaurants, and activities
4. **coordinate_bookings** - Help coordinate reservations for restaurants, events, and accommodations
5. **execute_agent_task** - Execute specialized tasks using different AI agents (product, info, booking, orchestrator)

### Key Components

- **MCP Server** (`src/planner/mcp_server.py`) - Full MCP protocol implementation
- **Gemini Tools** (`src/planner/gemini_tools.py`) - Direct Gemini API integration with function calling
- **API Handler** (`src/planner/tools_api_handler.py`) - Standalone tool execution without dependencies
- **Configuration** (`src/planner/mcp_config.py`) - Comprehensive configuration management

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_mcp.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Required:**
- `GOOGLE_API_KEY` - Your Google AI API key

**Optional:**
- `SERPER_API_KEY` - For enhanced web search
- `OPENAI_API_KEY` - Alternative AI provider
- `AMADEUS_API_KEY` - For real flight/hotel data

### 3. Test the Tools

```bash
# Test tools directly
python test_gemini_tools.py

# Start MCP server
python start_mcp_server.py
```

## 🛠️ Usage Examples

### Direct Gemini Integration

```python
import asyncio
from src.planner.gemini_tools import TravelPlanningGeminiTools

async def example():
    tools = TravelPlanningGeminiTools("your-api-key")
    chat = await tools.create_chat_session()
    
    response = await tools.process_chat_with_tools(
        chat,
        "Plan a 7-day trip to Tokyo for $3000 with cultural focus"
    )
    print(response)

asyncio.run(example())
```

### MCP Server Integration

```bash
# Start the MCP server
python start_mcp_server.py

# The server will be available via stdio for MCP clients
```

### Direct API Usage

```python
import asyncio
from src.planner.tools_api_handler import TravelPlanningToolsAPI

async def example():
    api = TravelPlanningToolsAPI()
    
    result = await api.create_travel_plan({
        "destination": "Paris, France",
        "travel_dates": "June 1-7, 2025",
        "budget": "$2500",
        "travel_style": "cultural",
        "group_size": 2
    })
    
    print(result)

asyncio.run(example())
```

## 📋 Tool Specifications

### create_travel_plan

Creates comprehensive travel plans including itineraries, product recommendations, local experiences, and booking information.

**Parameters:**
- `destination` (string, required) - Travel destination
- `travel_dates` (string, required) - Travel dates
- `budget` (string, required) - Budget range
- `travel_style` (string, required) - Travel style (adventure, cultural, relaxation, etc.)
- `group_size` (integer, optional) - Number of travelers (default: 1)

**Response:**
```json
{
  "success": true,
  "data": {
    "destination": "Tokyo, Japan",
    "itinerary": [...],
    "product_recommendations": [...],
    "local_experiences": [...],
    "booking_info": [...],
    "packing_checklist": [...],
    "budget_breakdown": {...},
    "tips": [...]
  }
}
```

### search_travel_products

Search for travel-related products and gear recommendations.

**Parameters:**
- `query` (string, required) - Product search query
- `budget` (string, required) - Budget constraint
- `destination` (string, optional) - Travel destination for context
- `travel_dates` (string, optional) - Travel dates for context

### discover_local_experiences

Discover local experiences, events, restaurants, and attractions.

**Parameters:**
- `location` (string, required) - Location to discover
- `interests` (array, required) - List of interests
- `travel_dates` (string, optional) - Travel dates
- `budget` (string, optional) - Budget constraint

### coordinate_bookings

Coordinate bookings and reservations for various venues and activities.

**Parameters:**
- `location` (string, required) - Location for bookings
- `booking_types` (array, required) - Types of bookings (restaurant, event, activity, etc.)
- `travel_dates` (string, required) - Travel dates
- `preferences` (object, optional) - Booking preferences

### execute_agent_task

Execute specific tasks using specialized AI agents.

**Parameters:**
- `agent_type` (string, required) - Agent type (product, info, booking, orchestrator)
- `task_description` (string, required) - Detailed task description
- `context` (object, optional) - Additional context

## ⚙️ Configuration

### Environment Variables

```bash
# Core Configuration
GOOGLE_API_KEY=your_google_api_key_here
ENABLE_MOCK_MODE=false  # Set to true for testing

# Server Settings
MCP_SERVER_NAME=travel-planning-mcp
MCP_SERVER_VERSION=1.0.0
LOG_LEVEL=INFO

# AI Model Settings
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_TEMPERATURE=0.7

# Optional APIs
SERPER_API_KEY=your_serper_api_key
AMADEUS_API_KEY=your_amadeus_api_key
```

### Configuration Validation

```bash
python -c "from src.planner.mcp_config import validate_configuration; print(validate_configuration())"
```

## 🏗️ Architecture

### MCP Server Flow

1. **Client Request** → MCP Protocol → **Tool Execution**
2. **Tool Handler** → **API Logic** → **AI Service** (Gemini/CrewAI)
3. **Response Processing** → **MCP Protocol** → **Client Response**

### Direct Gemini Flow

1. **Chat Message** → **Gemini API** → **Function Call Detection**
2. **Tool Execution** → **Result Processing** → **Function Response**
3. **Gemini Processing** → **Final Response** → **Client**

### Components

```
src/planner/
├── mcp_server.py          # MCP protocol server
├── gemini_tools.py        # Direct Gemini integration
├── tools_api_handler.py   # Standalone tool execution
├── mcp_config.py          # Configuration management
├── models.py              # Data models
└── services/
    └── crew_service.py    # CrewAI agent services
```

## 🧪 Testing

### Run All Tests

```bash
python test_gemini_tools.py
```

### Test Individual Components

```bash
# Test configuration
python src/planner/mcp_config.py

# Test direct tools
python src/planner/tools_api_handler.py

# Test MCP server (requires MCP client)
python start_mcp_server.py
```

## 🔧 Development

### Adding New Tools

1. **Define Tool Schema** in `gemini_tools.py`
2. **Add Handler Method** in `tools_api_handler.py`
3. **Register Tool** in `mcp_server.py`
4. **Update Tests** in `test_gemini_tools.py`

### Mock vs Production Mode

- **Mock Mode**: Returns simulated data for testing
- **Production Mode**: Uses real APIs and AI services

Toggle with `ENABLE_MOCK_MODE` environment variable.

## 📚 Integration Examples

### Claude Code Integration

```python
# In your Claude Code MCP configuration
{
  "mcpServers": {
    "travel-planning": {
      "command": "python",
      "args": ["start_mcp_server.py"],
      "cwd": "/path/to/planner.io"
    }
  }
}
```

### Gemini API Direct Usage

```python
import google.generativeai as genai
from src.planner.gemini_tools import TravelPlanningGeminiTools

genai.configure(api_key="your-api-key")
tools = TravelPlanningGeminiTools("your-api-key")

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    tools=tools.get_tools()
)

chat = model.start_chat()
response = chat.send_message("Plan a trip to Tokyo")
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   # Check API key
   echo $GOOGLE_API_KEY
   # Validate configuration
   python src/planner/mcp_config.py
   ```

2. **Import Errors**
   ```bash
   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:./src"
   ```

3. **MCP Connection Issues**
   ```bash
   # Test server startup
   python start_mcp_server.py --help
   ```

### Logs

- **Console**: Real-time logging to stdout
- **File**: `logs/mcp_server.log` (if enabled)

## 📄 License

This project is part of the TripMaxx travel planning application. See the main project README for license information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test output
3. Check the logs for detailed error information
4. Open an issue with full error details and configuration