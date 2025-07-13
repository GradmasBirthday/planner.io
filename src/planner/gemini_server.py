#!/usr/bin/env python3
"""
FastAPI server for Gemini API proxy
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Gemini API Proxy", version="1.0.0")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

@app.get("/")
async def root():
    return {"message": "Gemini API Proxy is running", "status": "healthy"}

@app.post("/chat")
async def chat(req: ChatRequest):
    """
    Handle chat requests and forward to Gemini API
    """
    # Check if the message is travel-related
    travel_keywords = [
        'travel', 'trip', 'vacation', 'holiday', 'destination', 'visit', 'go to',
        'plan', 'itinerary', 'booking', 'hotel', 'flight', 'accommodation',
        'tourist', 'sightseeing', 'explore', 'adventure', 'journey'
    ]
    
    user_message_lower = req.message.lower()
    is_travel_related = any(keyword in user_message_lower for keyword in travel_keywords)
    
    if is_travel_related:
        # Travel planning prompt
        prompt = f"""You are a helpful travel planning assistant. The user said: "{req.message}"

Please provide a detailed, well-formatted response that includes:
1. Personalized travel recommendations based on their request
2. A suggested itinerary if they mention a specific destination
3. Practical travel tips and advice
4. Budget considerations if mentioned
5. Cultural insights and local recommendations

Format your response with:
- Clear headings using markdown (## for main sections)
- Bullet points for lists
- Bold text for important information
- Proper spacing between sections
- A friendly, helpful tone

Keep your response engaging and easy to read."""
    else:
        # General conversation prompt
        prompt = f"""You are a friendly, helpful AI assistant. The user said: "{req.message}"

Please respond naturally and conversationally. Don't try to sell travel services unless the user specifically asks about travel planning.

Format your response with:
- Clear, readable text
- Proper spacing
- A warm, conversational tone
- Helpful information without being pushy

Just have a normal conversation with the user."""
    
    try:
        response = model.generate_content(prompt)
        return {
            "success": True, 
            "message": response.text, 
            "powered_by": "Google Gemini"
        }
    except Exception as e:
        return {
            "success": False, 
            "error": str(e), 
            "message": "Failed to get response from Gemini."
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "gemini-proxy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 