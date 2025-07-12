#!/usr/bin/env python3
"""
API handler for connecting frontend chat to CrewAI agents with Gemini
"""
import json
import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from planner.crew import Planner

# Load environment variables from .env file
load_dotenv()

def extract_travel_params(message: str) -> dict:
    """
    Extract travel parameters from user message using simple keyword matching.
    In production, this would use more sophisticated NLP.
    """
    message_lower = message.lower()
    
    # Default parameters
    params = {
        'destination': 'Tokyo, Japan',
        'duration': '5',
        'travel_style': 'cultural exploration',
        'budget': '$2000-3000',
        'interests': 'local culture, food, sightseeing',
        'accommodation_type': 'mid-range hotels'
    }
    
    # Extract destination
    if 'tokyo' in message_lower or 'japan' in message_lower:
        params['destination'] = 'Tokyo, Japan'
        params['travel_style'] = 'foodie and cultural exploration'
    elif 'paris' in message_lower or 'france' in message_lower:
        params['destination'] = 'Paris, France'
        params['travel_style'] = 'cultural and romantic'
    elif 'bali' in message_lower or 'indonesia' in message_lower:
        params['destination'] = 'Bali, Indonesia'
        params['travel_style'] = 'wellness and adventure'
    elif 'london' in message_lower or 'england' in message_lower:
        params['destination'] = 'London, England'
        params['travel_style'] = 'historical and cultural'
    
    # Extract duration
    if 'week' in message_lower or '7 day' in message_lower:
        params['duration'] = '7'
    elif '3 day' in message_lower or 'weekend' in message_lower:
        params['duration'] = '3'
    elif '10 day' in message_lower:
        params['duration'] = '10'
    
    # Extract travel style
    if 'food' in message_lower or 'culinary' in message_lower:
        params['travel_style'] = 'foodie exploration'
        params['interests'] = 'authentic cuisine, local markets, cooking classes'
    elif 'adventure' in message_lower:
        params['travel_style'] = 'adventure and outdoor'
        params['interests'] = 'hiking, outdoor activities, nature'
    elif 'relax' in message_lower or 'wellness' in message_lower:
        params['travel_style'] = 'wellness and relaxation'
        params['interests'] = 'spa, yoga, peaceful environments'
    elif 'culture' in message_lower or 'history' in message_lower:
        params['travel_style'] = 'cultural and historical'
        params['interests'] = 'museums, historical sites, local culture'
    
    # Extract budget hints
    if 'budget' in message_lower or 'cheap' in message_lower:
        params['budget'] = '$1000-2000'
        params['accommodation_type'] = 'hostels and budget hotels'
    elif 'luxury' in message_lower or 'expensive' in message_lower:
        params['budget'] = '$5000+'
        params['accommodation_type'] = 'luxury hotels and resorts'
    
    return params

def run_travel_planning(message: str) -> dict:
    """
    Run travel planning using Gemini directly (bypassing CrewAI for now due to compatibility issues)
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Extract parameters from user message
        params = extract_travel_params(message)
        
        # Initialize Gemini directly
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found")
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Create detailed travel planning prompt
        prompt = f"""
You are an expert travel planner. Create a detailed {params['duration']}-day itinerary for {params['destination']} 
based on these preferences:
- Travel Style: {params['travel_style']}
- Budget: {params['budget']}
- Interests: {params['interests']}
- Accommodation: {params['accommodation_type']}

Please provide:
1. Day-by-day itinerary with specific activities and timing
2. Restaurant recommendations for each day
3. Estimated costs for activities
4. Travel tips and cultural insights
5. Accommodation suggestions

Format the response in a clear, detailed manner that's helpful for trip planning.
"""
        
        # Get response from Gemini
        response = llm.invoke(prompt)
        
        return {
            'success': True,
            'message': f"I've created a personalized {params['duration']}-day itinerary for {params['destination']} powered by Gemini AI!\n\n{response.content}",
            'params': params,
            'full_result': response.content,
            'powered_by': 'Google Gemini'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"I encountered an issue while planning your trip: {str(e)}. Let me help you with a basic recommendation instead."
        }

def main():
    """
    Main function for CLI usage
    """
    if len(sys.argv) < 2:
        print("Usage: python api_handler.py '<user_message>'")
        sys.exit(1)
    
    user_message = sys.argv[1]
    result = run_travel_planning(user_message)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()