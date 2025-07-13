"""
Simple Local Discovery API - Standalone FastAPI server without CrewAI dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime

# Import the local discovery service directly
from src.planner.services.local_discovery_service import LocalDiscoveryService

app = FastAPI(
    title="Local Discovery API",
    description="Standalone API for discovering local attractions, restaurants, and experiences",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LocalDiscoveryRequest(BaseModel):
    location: str
    interests: List[str] = []
    travel_dates: Optional[str] = None
    budget: Optional[str] = None

class LocalDiscoveryResponse(BaseModel):
    success: bool
    message: str
    data: dict
    
    class Config:
        # Allow arbitrary types for the LocalDiscoveryData object
        arbitrary_types_allowed = True

# Initialize the service
discovery_service = LocalDiscoveryService()

@app.get("/")
async def root():
    return {"message": "Local Discovery API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/local/discover", response_model=LocalDiscoveryResponse)
async def discover_local(request: LocalDiscoveryRequest):
    """
    Discover local attractions, restaurants, and experiences
    """
    try:
        result = await discovery_service.discover_places(
            location=request.location,
            interests=request.interests,
            travel_dates=request.travel_dates,
            budget=request.budget
        )
        return LocalDiscoveryResponse(
            success=True,
            message="Local discovery completed successfully",
            data=result.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": exc.detail, "status_code": exc.status_code}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {"error": "Internal server error", "details": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 