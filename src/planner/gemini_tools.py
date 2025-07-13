"""
Gemini API Tools for Travel Planning

This module defines tools that can be used directly with Google's Gemini API
for travel planning functionality. These tools follow the Gemini function calling specification.
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

from .models import (
    TravelPlanRequest, ProductSearchRequest, LocalDiscoveryRequest,
    BookingRequest, AgentTaskRequest, TravelStyle, BookingType, AgentType
)
from .services.crew_service import TravelPlanningService

logger = logging.getLogger(__name__)

class TravelPlanningGeminiTools:
    """Gemini tools for travel planning"""

    def __init__(self, api_key: str):
        """Initialize Gemini tools with API key"""
        genai.configure(api_key=api_key)
        self.travel_service = TravelPlanningService()
        self.tools = self._create_tools()

    def _create_tools(self) -> List[Tool]:
        """Create Gemini function declarations for travel planning"""

        # Travel Plan Creation Function
        create_travel_plan_func = FunctionDeclaration(
            name="create_travel_plan",
            description="Create a comprehensive travel plan for a destination including itinerary, product recommendations, local experiences, and booking information",
            parameters={
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "Travel destination (e.g., 'Tokyo, Japan', 'Paris, France')"
                    },
                    "travel_dates": {
                        "type": "string",
                        "description": "Travel dates (e.g., 'March 15-22, 2025', 'July 1-10, 2025')"
                    },
                    "budget": {
                        "type": "string",
                        "description": "Budget range (e.g., '$2000-3000', '$500-1000', '$5000+')"
                    },
                    "travel_style": {
                        "type": "string",
                        "description": "Travel style preference",
                        "enum": [style.value for style in TravelStyle]
                    },
                    "group_size": {
                        "type": "integer",
                        "description": "Number of travelers",
                        "default": 1
                    }
                },
                "required": ["destination", "travel_dates", "budget", "travel_style"]
            }
        )

        # Product Search Function
        search_travel_products_func = FunctionDeclaration(
            name="search_travel_products",
            description="Search for travel-related products and gear recommendations from Amazon and other platforms",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product search query (e.g., 'waterproof hiking boots', 'travel backpack 40L')"
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

        # Local Discovery Function
        discover_local_experiences_func = FunctionDeclaration(
            name="discover_local_experiences",
            description="Discover local experiences, events, restaurants, and attractions based on interests and location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to discover (e.g., 'Tokyo', 'Paris 15th arrondissement')"
                    },
                    "interests": {
                        "type": "array",
                        "description": "List of interests (e.g., ['food', 'art', 'nightlife', 'history'])",
                        "items": {"type": "string"}
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

        # Booking Coordination Function
        coordinate_bookings_func = FunctionDeclaration(
            name="coordinate_bookings",
            description="Coordinate bookings and reservations for restaurants, events, activities, and accommodations",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location for bookings"
                    },
                    "booking_types": {
                        "type": "array",
                        "description": "Types of bookings needed",
                        "items": {
                            "type": "string",
                            "enum": [booking_type.value for booking_type in BookingType]
                        }
                    },
                    "travel_dates": {
                        "type": "string",
                        "description": "Travel dates for booking timing"
                    },
                    "preferences": {
                        "type": "object",
                        "description": "Booking preferences (optional)"
                    }
                },
                "required": ["location", "booking_types", "travel_dates"]
            }
        )

        # Agent Task Execution Function
        execute_agent_task_func = FunctionDeclaration(
            name="execute_agent_task",
            description="Execute a specific task with a designated travel planning agent",
            parameters={
                "type": "object",
                "properties": {
                    "agent_type": {
                        "type": "string",
                        "description": "Type of agent to use",
                        "enum": [agent_type.value for agent_type in AgentType]
                    },
                    "task_description": {
                        "type": "string",
                        "description": "Detailed task description"
                    },
                    "context": {
                        "type": "object",
                        "description": "Additional context for the task (optional)"
                    }
                },
                "required": ["agent_type", "task_description"]
            }
        )

        # Create tool objects
        travel_planning_tool = Tool(
            function_declarations=[
                create_travel_plan_func,
                search_travel_products_func,
                discover_local_experiences_func,
                coordinate_bookings_func,
                execute_agent_task_func
            ]
        )

        return [travel_planning_tool]

    async def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function call from Gemini"""
        try:
            logger.info(f"Executing function: {function_name} with arguments: {arguments}")

            if function_name == "create_travel_plan":
                return await self._handle_create_travel_plan(arguments)
            elif function_name == "search_travel_products":
                return await self._handle_search_products(arguments)
            elif function_name == "discover_local_experiences":
                return await self._handle_discover_local(arguments)
            elif function_name == "coordinate_bookings":
                return await self._handle_coordinate_booking(arguments)
            elif function_name == "execute_agent_task":
                return await self._handle_agent_task(arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown function: {function_name}",
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _handle_create_travel_plan(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle travel plan creation"""
        try:
            request = TravelPlanRequest(**arguments)
            result = await self.travel_service.create_travel_plan(
                destination=request.destination,
                travel_dates=request.travel_dates,
                budget=request.budget,
                travel_style=request.travel_style,
                group_size=request.group_size
            )

            return {
                "success": True,
                "message": "Travel plan created successfully",
                "data": result.dict(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error creating travel plan: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _handle_search_products(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle product search"""
        try:
            request = ProductSearchRequest(**arguments)
            result = await self.travel_service.search_products(
                query=request.query,
                budget=request.budget,
                destination=request.destination,
                travel_dates=request.travel_dates
            )

            return {
                "success": True,
                "message": "Product search completed successfully",
                "data": result.dict(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _handle_discover_local(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle local discovery"""
        try:
            request = LocalDiscoveryRequest(**arguments)
            result = await self.travel_service.discover_local(
                location=request.location,
                interests=request.interests,
                travel_dates=request.travel_dates,
                budget=request.budget
            )

            return {
                "success": True,
                "message": "Local discovery completed successfully",
                "data": result.dict(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error discovering local experiences: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _handle_coordinate_booking(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle booking coordination"""
        try:
            request = BookingRequest(**arguments)
            result = await self.travel_service.coordinate_booking(
                location=request.location,
                booking_types=request.booking_types,
                travel_dates=request.travel_dates,
                preferences=request.preferences
            )

            return {
                "success": True,
                "message": "Booking coordination completed successfully",
                "data": result.dict(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error coordinating bookings: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _handle_agent_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle agent task execution"""
        try:
            request = AgentTaskRequest(**arguments)
            result = await self.travel_service.execute_agent_task(
                agent_type=request.agent_type,
                task_description=request.task_description,
                context=request.context
            )

            return {
                "success": True,
                "message": f"Agent task executed successfully by {request.agent_type} agent",
                "data": result.dict(),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error executing agent task: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def get_tools(self) -> List[Tool]:
        """Get the list of tools for Gemini"""
        return self.tools

    async def create_chat_session(self, model_name: str = "gemini-2.0-flash-exp") -> Any:
        """Create a Gemini chat session with tools enabled"""
        model = genai.GenerativeModel(
            model_name=model_name,
            tools=self.tools
        )
        return model.start_chat()

    async def process_chat_with_tools(self, chat_session: Any, message: str) -> str:
        """Process a chat message with tool execution"""
        try:
            # Send message to Gemini
            response = chat_session.send_message(message)

            # Check if Gemini wants to use tools
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        # Execute the function call
                        function_call = part.function_call
                        function_result = await self.execute_function(
                            function_call.name,
                            dict(function_call.args)
                        )

                        # Send the function result back to Gemini
                        response = chat_session.send_message(
                            genai.protos.Content(
                                parts=[genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=function_call.name,
                                        response={"result": function_result}
                                    )
                                )]
                            )
                        )

            return response.text

        except Exception as e:
            logger.error(f"Error processing chat with tools: {str(e)}")
            return f"Error processing your request: {str(e)}"


# Example usage functions
async def example_travel_planning_chat():
    """Example of using Gemini with travel planning tools"""
    import os
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Please set GOOGLE_API_KEY environment variable")
        return

    tools = TravelPlanningGeminiTools(api_key)
    chat = await tools.create_chat_session()

    # Example conversation
    response = await tools.process_chat_with_tools(
        chat,
        "I want to plan a 7-day trip to Tokyo in March 2025. My budget is $3000 and I'm interested in cultural experiences and food. Can you help me create a comprehensive travel plan?"
    )

    print("Gemini Response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(example_travel_planning_chat())