"""
Travel Planning API - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, List, Any, Optional
import asyncio
from contextlib import asynccontextmanager

from .models import (
    TravelPlanRequest, TravelPlanResponse,
    ProductSearchRequest, ProductSearchResponse,
    LocalDiscoveryRequest, LocalDiscoveryResponse,
    BookingRequest, BookingResponse,
    AgentTaskRequest, AgentTaskResponse
)
from .services.crew_service import TravelPlanningService
from .config import settings

# Global service instance
travel_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global travel_service
    # Startup
    travel_service = TravelPlanningService()
    yield
    # Shutdown
    travel_service = None

app = FastAPI(
    title="Travel Planning API",
    description="A comprehensive travel planning system with specialized agents for product recommendations, local discovery, and booking coordination",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for background tasks
task_results: Dict[str, Any] = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Travel Planning API",
        "version": "1.0.0",
        "endpoints": {
            "travel_plan": "/api/v1/travel/plan",
            "product_search": "/api/v1/products/search",
            "local_discovery": "/api/v1/local/discover",
            "booking": "/api/v1/booking/coordinate",
            "agent_task": "/api/v1/agent/task"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "travel-planning-api"}

# Travel Planning Endpoints
@app.post("/api/v1/travel/plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest):
    """
    Create a comprehensive travel plan for a destination
    
    This endpoint orchestrates all agents to create a complete travel plan including:
    - Product recommendations
    - Local discoveries
    - Booking coordination
    - Integrated itinerary
    """
    try:
        if not travel_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await travel_service.create_travel_plan(
            destination=request.destination,
            travel_dates=request.travel_dates,
            budget=request.budget,
            travel_style=request.travel_style,
            group_size=request.group_size
        )
        
        return TravelPlanResponse(
            success=True,
            message="Travel plan created successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/travel/plan/async")
async def create_travel_plan_async(request: TravelPlanRequest, background_tasks: BackgroundTasks):
    """
    Create a comprehensive travel plan asynchronously
    Returns a task ID to check status
    """
    try:
        if not travel_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        import uuid
        task_id = str(uuid.uuid4())
        
        # Add background task
        background_tasks.add_task(
            _create_travel_plan_background,
            task_id,
            request
        )
        
        return {"task_id": task_id, "status": "processing", "message": "Travel plan creation started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def _create_travel_plan_background(task_id: str, request: TravelPlanRequest):
    """Background task for creating travel plan"""
    try:
        result = await travel_service.create_travel_plan(
            destination=request.destination,
            travel_dates=request.travel_dates,
            budget=request.budget,
            travel_style=request.travel_style,
            group_size=request.group_size
        )
        task_results[task_id] = {"status": "completed", "result": result}
    except Exception as e:
        task_results[task_id] = {"status": "failed", "error": str(e)}

@app.get("/api/v1/travel/plan/status/{task_id}")
async def get_travel_plan_status(task_id: str):
    """Get the status of an async travel plan creation task"""
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_results[task_id]

# Product Search Endpoints
@app.post("/api/v1/products/search", response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest):
    """
    Search for travel-related products
    
    Find and recommend products from Amazon and other platforms based on:
    - Query description
    - Budget constraints
    - Travel requirements
    """
    try:
        if not travel_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await travel_service.search_products(
            query=request.query,
            budget=request.budget,
            destination=request.destination,
            travel_dates=request.travel_dates
        )
        
        return ProductSearchResponse(
            success=True,
            message="Product search completed successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Local Discovery Endpoints
@app.post("/api/v1/local/discover", response_model=LocalDiscoveryResponse)
async def discover_local(request: LocalDiscoveryRequest):
    """
    Discover local experiences and opportunities
    
    Find local events, restaurants, attractions, and deals based on:
    - Location
    - Interests
    - Travel dates
    """
    try:
        if not travel_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await travel_service.discover_local(
            location=request.location,
            interests=request.interests,
            travel_dates=request.travel_dates,
            budget=request.budget
        )
        
        return LocalDiscoveryResponse(
            success=True,
            message="Local discovery completed successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Booking Endpoints
@app.post("/api/v1/booking/coordinate", response_model=BookingResponse)
async def coordinate_booking(request: BookingRequest):
    """
    Coordinate bookings and reservations
    
    Handle booking coordination for:
    - Restaurant reservations
    - Event tickets
    - Activity bookings
    - Tours and experiences
    """
    try:
        if not travel_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await travel_service.coordinate_booking(
            location=request.location,
            booking_types=request.booking_types,
            travel_dates=request.travel_dates,
            preferences=request.preferences
        )
        
        return BookingResponse(
            success=True,
            message="Booking coordination completed successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agent Task Endpoints
@app.post("/api/v1/agent/task", response_model=AgentTaskResponse)
async def execute_agent_task(request: AgentTaskRequest):
    """
    Execute a specific task with a designated agent
    
    Available agents:
    - product: Product search and recommendations
    - info: Local information and event discovery
    - booking: Booking and reservation coordination
    - orchestrator: Travel planning orchestration
    """
    try:
        if not travel_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await travel_service.execute_agent_task(
            agent_type=request.agent_type,
            task_description=request.task_description,
            context=request.context
        )
        
        return AgentTaskResponse(
            success=True,
            message=f"Agent task executed successfully by {request.agent_type} agent",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Additional utility endpoints
@app.get("/api/v1/agents")
async def get_available_agents():
    """Get list of available agents and their capabilities"""
    return {
        "agents": {
            "product": {
                "role": "Product Search and Recommendation Specialist",
                "capabilities": ["Product research", "Price comparison", "Review analysis", "Shopping platform integration"]
            },
            "info": {
                "role": "Local Information and Event Discovery Specialist",
                "capabilities": ["Local event discovery", "Restaurant recommendations", "Attraction research", "Deal finding"]
            },
            "booking": {
                "role": "Booking and Reservation Coordinator",
                "capabilities": ["Reservation coordination", "Booking management", "Alternative options", "Policy guidance"]
            },
            "orchestrator": {
                "role": "Travel Planning Orchestrator",
                "capabilities": ["Plan coordination", "Task prioritization", "Integration management", "Comprehensive planning"]
            }
        }
    }

@app.get("/api/v1/destinations/popular")
async def get_popular_destinations():
    """Get list of popular travel destinations"""
    return {
        "destinations": [
            "Tokyo, Japan",
            "Paris, France",
            "New York, USA",
            "London, UK",
            "Barcelona, Spain",
            "Rome, Italy",
            "Bangkok, Thailand",
            "Dubai, UAE",
            "Sydney, Australia",
            "Amsterdam, Netherlands"
        ]
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 