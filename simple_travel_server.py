#!/usr/bin/env python3
"""
Simple Travel Planning API Server
Bypasses CrewAI to avoid dependency conflicts
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="TripMaxx Travel Planning API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TravelPlanRequest(BaseModel):
    destination: str
    travel_dates: str
    budget: str
    travel_style: str
    group_size: int = 1

class ChatRequest(BaseModel):
    message: str

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment")

try:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except ImportError:
    print("Warning: google-generativeai not available, using mock responses")
    model = None

@app.get("/")
async def root():
    return {
        "message": "TripMaxx Travel Planning API",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "travel_plan": "/api/v1/travel/plan",
            "chat": "/chat",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "travel-planning-api"}

@app.post("/api/v1/travel/plan")
async def create_travel_plan(request: TravelPlanRequest):
    """Create a comprehensive travel plan"""
    try:
        # Create a detailed travel planning prompt
        prompt = f"""
You are an expert travel planner. Create a comprehensive travel plan for:

**Destination**: {request.destination}
**Travel Dates**: {request.travel_dates}
**Budget**: {request.budget}
**Travel Style**: {request.travel_style}
**Group Size**: {request.group_size} people

Please provide a detailed response with:

## 🗓️ Daily Itinerary
- Day-by-day activities with specific timing
- Must-see attractions and experiences
- Cultural highlights and local insights

## 🍽️ Dining Recommendations
- Local cuisine specialties to try
- Restaurant recommendations for different budgets
- Food markets and street food options

## 🏨 Accommodation Suggestions
- Hotels/accommodations that fit the budget and style
- Best neighborhoods to stay in
- Booking tips and alternatives

## 💰 Budget Breakdown
- Estimated costs for activities, meals, and transportation
- Money-saving tips and free activities
- Budget allocation recommendations

## 🎯 Local Experiences
- Unique activities and hidden gems
- Cultural experiences and local traditions
- Seasonal activities and events

## 🚗 Transportation
- Getting around the destination
- Airport transfers and local transport
- Travel passes and cost-effective options

## 📝 Travel Tips
- Best time to visit and weather considerations
- Cultural etiquette and local customs
- Safety tips and emergency contacts
- Packing recommendations

## 📱 Useful Apps and Resources
- Local apps for navigation and dining
- Booking platforms and resources
- Language apps if needed

Format your response with clear headings, bullet points, and practical advice. Make it engaging and easy to follow!
"""

        # Get response from Gemini
        response = model.generate_content(prompt)
        
        return {
            "success": True,
            "message": response.text,
            "data": {
                "destination": request.destination,
                "travel_dates": request.travel_dates,
                "budget": request.budget,
                "travel_style": request.travel_style,
                "group_size": request.group_size,
                "itinerary": response.text,
                "powered_by": "Google Gemini"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating travel plan: {str(e)}")

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat requests for travel planning"""
    try:
        # Check if message is travel-related
        travel_keywords = [
            'travel', 'trip', 'vacation', 'holiday', 'destination', 'visit', 
            'plan', 'itinerary', 'booking', 'hotel', 'flight', 'tokyo', 
            'paris', 'london', 'bali', 'where', 'budget'
        ]
        
        message_lower = request.message.lower()
        is_travel_related = any(keyword in message_lower for keyword in travel_keywords)
        
        if is_travel_related:
            prompt = f"""You are a helpful travel planning assistant. The user said: "{request.message}"

Please provide a personalized travel response that includes:
1. Destination recommendations if they're asking where to go
2. Budget-friendly suggestions if they mention cost concerns
3. Activity recommendations based on their interests
4. Practical travel tips and advice
5. Next steps for planning their trip

Keep your response conversational, helpful, and engaging. Use emojis and formatting to make it easy to read.
"""
        else:
            prompt = f"""You are a friendly AI assistant. The user said: "{request.message}"

Respond naturally and helpfully. If they're not asking about travel, just have a normal conversation.
"""
        
        response = model.generate_content(prompt)
        
        return {
            "success": True,
            "message": response.text,
            "powered_by": "Google Gemini"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 