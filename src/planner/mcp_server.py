"""
MCP Server for Travel Planning Tools

This server exposes travel planning functionality as tools that can be called by Gemini AI.
Based on the Model Context Protocol (MCP) specification.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from .models import (
    TravelPlanRequest, ProductSearchRequest, LocalDiscoveryRequest,
    BookingRequest, AgentTaskRequest, TravelStyle, BookingType, AgentType
)
from .tools_api_handler import TravelPlanningToolsAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global service instance
travel_service: Optional[TravelPlanningToolsAPI] = None

class TravelPlanningMCPServer:
    """MCP Server for travel planning tools"""

    def __init__(self):
        self.server = Server("travel-planning-mcp")
        self.setup_tools()
        self.setup_handlers()

    def setup_tools(self):
        """Define the tools available to Gemini"""

        # Travel Plan Creation Tool
        travel_plan_tool = Tool(
            name="create_travel_plan",
            description="Create a comprehensive travel plan for a destination including itinerary, product recommendations, local experiences, and booking information",
            inputSchema={
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "Travel destination (e.g., 'Tokyo, Japan', 'Paris, France')",
                        "minLength": 2,
                        "maxLength": 100
                    },
                    "travel_dates": {
                        "type": "string",
                        "description": "Travel dates (e.g., 'March 15-22, 2025', 'July 1-10, 2025')",
                        "minLength": 5
                    },
                    "budget": {
                        "type": "string",
                        "description": "Budget range (e.g., '$2000-3000', '$500-1000', '$5000+')",
                        "minLength": 1
                    },
                    "travel_style": {
                        "type": "string",
                        "description": "Travel style preference",
                        "enum": [style.value for style in TravelStyle]
                    },
                    "group_size": {
                        "type": "integer",
                        "description": "Number of travelers",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 1
                    }
                },
                "required": ["destination", "travel_dates", "budget", "travel_style"]
            }
        )

        # Product Search Tool
        product_search_tool = Tool(
            name="search_travel_products",
            description="Search for travel-related products and gear recommendations from Amazon and other platforms",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product search query (e.g., 'waterproof hiking boots', 'travel backpack 40L')",
                        "minLength": 2,
                        "maxLength": 200
                    },
                    "budget": {
                        "type": "string",
                        "description": "Budget constraint (e.g., '$50-100', 'under $200')"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Travel destination for context (optional)"
                    },
                    "travel_dates": {
                        "type": "string",
                        "description": "Travel dates for context (optional)"
                    }
                },
                "required": ["query", "budget"]
            }
        )

        # Local Discovery Tool
        local_discovery_tool = Tool(
            name="discover_local_experiences",
            description="Discover local experiences, events, restaurants, and attractions based on interests and location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to discover (e.g., 'Tokyo', 'Paris 15th arrondissement')",
                        "minLength": 2,
                        "maxLength": 100
                    },
                    "interests": {
                        "type": "array",
                        "description": "List of interests (e.g., ['food', 'art', 'nightlife', 'history'])",
                        "items": {"type": "string"},
                        "minItems": 1
                    },
                    "travel_dates": {
                        "type": "string",
                        "description": "Travel dates for event timing (optional)"
                    },
                    "budget": {
                        "type": "string",
                        "description": "Budget constraint (optional)"
                    }
                },
                "required": ["location", "interests"]
            }
        )

        # Booking Coordination Tool
        booking_coordination_tool = Tool(
            name="coordinate_bookings",
            description="Coordinate bookings and reservations for restaurants, events, activities, and accommodations",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location for bookings",
                        "minLength": 2,
                        "maxLength": 100
                    },
                    "booking_types": {
                        "type": "array",
                        "description": "Types of bookings needed",
                        "items": {
                            "type": "string",
                            "enum": [booking_type.value for booking_type in BookingType]
                        },
                        "minItems": 1
                    },
                    "travel_dates": {
                        "type": "string",
                        "description": "Travel dates for booking timing"
                    },
                    "preferences": {
                        "type": "object",
                        "description": "Booking preferences (optional)",
                        "additionalProperties": True
                    }
                },
                "required": ["location", "booking_types", "travel_dates"]
            }
        )

        # Agent Task Execution Tool
        agent_task_tool = Tool(
            name="execute_agent_task",
            description="Execute a specific task with a designated travel planning agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_type": {
                        "type": "string",
                        "description": "Type of agent to use",
                        "enum": [agent_type.value for agent_type in AgentType]
                    },
                    "task_description": {
                        "type": "string",
                        "description": "Detailed task description",
                        "minLength": 5,
                        "maxLength": 500
                    },
                    "context": {
                        "type": "object",
                        "description": "Additional context for the task (optional)",
                        "additionalProperties": True
                    }
                },
                "required": ["agent_type", "task_description"]
            }
        )

        # Register tools with the server
        self.server.list_tools = lambda: [
            travel_plan_tool,
            product_search_tool,
            local_discovery_tool,
            booking_coordination_tool,
            agent_task_tool
        ]

    def setup_handlers(self):
        """Setup tool execution handlers"""

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool execution requests"""
            try:
                global travel_service
                if not travel_service:
                    travel_service = TravelPlanningToolsAPI()

                logger.info(f"Executing tool: {name} with arguments: {arguments}")

                if name == "create_travel_plan":
                    return await self._handle_create_travel_plan(arguments)
                elif name == "search_travel_products":
                    return await self._handle_search_products(arguments)
                elif name == "discover_local_experiences":
                    return await self._handle_discover_local(arguments)
                elif name == "coordinate_bookings":
                    return await self._handle_coordinate_booking(arguments)
                elif name == "execute_agent_task":
                    return await self._handle_agent_task(arguments)
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]

            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error executing tool {name}: {str(e)}"
                )]

    async def _handle_create_travel_plan(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle travel plan creation"""
        try:
            result = await travel_service.create_travel_plan(arguments)

            # result is already a formatted response from tools_api_handler
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]

        except Exception as e:
            logger.error(f"Error creating travel plan: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error creating travel plan: {str(e)}"
            )]

    async def _handle_search_products(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle product search"""
        try:
            result = await travel_service.search_travel_products(arguments)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]

        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error searching products: {str(e)}"
            )]

    async def _handle_discover_local(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle local discovery"""
        try:
            result = await travel_service.discover_local_experiences(arguments)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]

        except Exception as e:
            logger.error(f"Error discovering local experiences: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error discovering local experiences: {str(e)}"
            )]

    async def _handle_coordinate_booking(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle booking coordination"""
        try:
            result = await travel_service.coordinate_bookings(arguments)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]

        except Exception as e:
            logger.error(f"Error coordinating bookings: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error coordinating bookings: {str(e)}"
            )]

    async def _handle_agent_task(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle agent task execution"""
        try:
            result = await travel_service.execute_agent_task(arguments)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]

        except Exception as e:
            logger.error(f"Error executing agent task: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error executing agent task: {str(e)}"
            )]

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="travel-planning-mcp",
                    server_version="1.0.0"
                )
            )


async def main():
    """Main entry point for the MCP server"""
    server = TravelPlanningMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())