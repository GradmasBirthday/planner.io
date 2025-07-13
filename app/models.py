"""
Pydantic models for Travel Planning API
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums for validation
class TravelStyle(str, Enum):
    """Travel style options"""
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    RELAXATION = "relaxation"
    BUSINESS = "business"
    BUDGET = "budget"
    LUXURY = "luxury"
    FAMILY = "family"
    SOLO = "solo"
    GROUP = "group"

class AgentType(str, Enum):
    """Available agent types"""
    PRODUCT = "product"
    INFO = "info"
    BOOKING = "booking"
    ORCHESTRATOR = "orchestrator"

class BookingType(str, Enum):
    """Types of bookings"""
    RESTAURANT = "restaurant"
    EVENT = "event"
    ACTIVITY = "activity"
    TOUR = "tour"
    ACCOMMODATION = "accommodation"
    TRANSPORT = "transport"

# Base response model
class BaseResponse(BaseModel):
    """Base response model"""
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

# Request Models
class TravelPlanRequest(BaseModel):
    """Request model for creating a travel plan"""
    destination: str = Field(..., min_length=2, max_length=100, description="Travel destination")
    travel_dates: str = Field(..., min_length=5, description="Travel dates (e.g., 'March 15-22, 2025')")
    budget: str = Field(..., min_length=1, description="Budget range (e.g., '$2000-3000')")
    travel_style: str = Field(..., description="Travel style preference")
    group_size: int = Field(1, ge=1, le=50, description="Number of travelers")
    
    @validator('destination')
    def validate_destination(cls, v):
        if not v.strip():
            raise ValueError('Destination cannot be empty')
        return v.strip()
    
    @validator('budget')
    def validate_budget(cls, v):
        if not v.strip():
            raise ValueError('Budget cannot be empty')
        return v.strip()

class ProductSearchRequest(BaseModel):
    """Request model for product search"""
    query: str = Field(..., min_length=2, max_length=200, description="Product search query")
    budget: str = Field(..., description="Budget constraint")
    destination: Optional[str] = Field(None, description="Travel destination for context")
    travel_dates: Optional[str] = Field(None, description="Travel dates for context")
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

class LocalDiscoveryRequest(BaseModel):
    """Request model for local discovery"""
    location: str = Field(..., min_length=2, max_length=100, description="Location to discover")
    interests: List[str] = Field(..., description="List of interests")
    travel_dates: Optional[str] = Field(None, description="Travel dates")
    budget: Optional[str] = Field(None, description="Budget constraint")
    
    @validator('location')
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()
    
    @validator('interests')
    def validate_interests(cls, v):
        if not v:
            raise ValueError('At least one interest is required')
        return [interest.strip() for interest in v if interest.strip()]

class BookingRequest(BaseModel):
    """Request model for booking coordination"""
    location: str = Field(..., min_length=2, max_length=100, description="Location for bookings")
    booking_types: List[BookingType] = Field(..., description="Types of bookings needed")
    travel_dates: str = Field(..., description="Travel dates")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Booking preferences")
    
    @validator('location')
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()

class AgentTaskRequest(BaseModel):
    """Request model for agent task execution"""
    agent_type: AgentType = Field(..., description="Type of agent to use")
    task_description: str = Field(..., min_length=5, max_length=500, description="Task description")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the task")
    
    @validator('task_description')
    def validate_task_description(cls, v):
        if not v.strip():
            raise ValueError('Task description cannot be empty')
        return v.strip()

# Response Models
class ProductRecommendation(BaseModel):
    """Product recommendation model"""
    name: str
    description: str
    price: str
    rating: Optional[float] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    features: List[str] = []
    pros: List[str] = []
    cons: List[str] = []
    why_recommended: str
    alternatives: List[str] = []

class LocalExperience(BaseModel):
    """Local experience model"""
    name: str
    description: str
    category: str
    location: str
    price_range: Optional[str] = None
    rating: Optional[float] = None
    opening_hours: Optional[str] = None
    booking_required: bool = False
    contact_info: Optional[str] = None
    why_recommended: str
    seasonal_info: Optional[str] = None

class BookingInfo(BaseModel):
    """Booking information model"""
    venue_name: str
    booking_type: BookingType
    description: str
    location: str
    price: Optional[str] = None
    booking_instructions: str
    deadline: Optional[str] = None
    cancellation_policy: Optional[str] = None
    alternatives: List[str] = []
    contact_info: str
    special_requirements: List[str] = []

class Itinerary(BaseModel):
    """Itinerary model"""
    day: int
    date: str
    activities: List[Dict[str, Any]]
    meals: List[Dict[str, Any]]
    notes: Optional[str] = None

class TravelPlanData(BaseModel):
    """Travel plan data model"""
    destination: str
    travel_dates: str
    budget: str
    group_size: int
    itinerary: List[Itinerary]
    product_recommendations: List[ProductRecommendation]
    local_experiences: List[LocalExperience]
    booking_info: List[BookingInfo]
    packing_checklist: List[str]
    budget_breakdown: Dict[str, str]
    emergency_contacts: List[str]
    tips: List[str]

class ProductSearchData(BaseModel):
    """Product search data model"""
    query: str
    total_results: int
    recommendations: List[ProductRecommendation]
    budget_summary: Dict[str, str]

class LocalDiscoveryData(BaseModel):
    """Local discovery data model"""
    location: str
    interests: List[str]
    total_results: int
    experiences: List[LocalExperience]
    events: List[Dict[str, Any]]
    restaurants: List[Dict[str, Any]]
    attractions: List[Dict[str, Any]]
    deals: List[Dict[str, Any]]

class BookingData(BaseModel):
    """Booking data model"""
    location: str
    booking_types: List[BookingType]
    total_bookings: int
    booking_info: List[BookingInfo]
    booking_timeline: List[Dict[str, Any]]
    priority_bookings: List[str]

class AgentTaskData(BaseModel):
    """Agent task data model"""
    agent_type: AgentType
    task_description: str
    result: Dict[str, Any]
    execution_time: float
    recommendations: List[str] = []

# Response Models
class TravelPlanResponse(BaseResponse):
    """Response model for travel plan"""
    data: TravelPlanData

class ProductSearchResponse(BaseResponse):
    """Response model for product search"""
    data: ProductSearchData

class LocalDiscoveryResponse(BaseResponse):
    """Response model for local discovery"""
    data: LocalDiscoveryData

class BookingResponse(BaseResponse):
    """Response model for booking coordination"""
    data: BookingData

class AgentTaskResponse(BaseResponse):
    """Response model for agent task execution"""
    data: AgentTaskData

# Error Models
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    status_code: int
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ValidationErrorResponse(BaseModel):
    """Validation error response model"""
    error: str = "Validation Error"
    status_code: int = 422
    detail: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.now) 