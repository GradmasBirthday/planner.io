from crewai.tools import BaseTool
from typing import Type, Dict, List
from pydantic import BaseModel, Field
import json


class DestinationResearchInput(BaseModel):
    """Input schema for destination research."""
    destination: str = Field(..., description="The destination to research (city, country)")
    travel_style: str = Field(..., description="Type of travel (adventure, cultural, wellness, foodie, etc.)")


class FlightSearchInput(BaseModel):
    """Input schema for flight search."""
    origin: str = Field(..., description="Origin city/airport")
    destination: str = Field(..., description="Destination city/airport")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: str = Field(None, description="Return date (YYYY-MM-DD) for round trip")
    budget_range: str = Field(..., description="Budget range (e.g., '$500-800')")


class HotelSearchInput(BaseModel):
    """Input schema for hotel search."""
    destination: str = Field(..., description="Destination city")
    checkin_date: str = Field(..., description="Check-in date (YYYY-MM-DD)")
    checkout_date: str = Field(..., description="Check-out date (YYYY-MM-DD)")
    accommodation_type: str = Field(..., description="Type of accommodation (hotel, hostel, resort, etc.)")
    budget_range: str = Field(..., description="Budget range per night")


class ActivitySearchInput(BaseModel):
    """Input schema for activity search."""
    destination: str = Field(..., description="Destination city")
    interests: str = Field(..., description="Traveler interests and preferences")
    travel_style: str = Field(..., description="Travel style (adventure, cultural, relaxed, etc.)")


class DestinationResearchTool(BaseTool):
    name: str = "Destination Research Tool"
    description: str = (
        "Research comprehensive information about a destination including attractions, "
        "culture, weather, local customs, and travel tips based on travel style."
    )
    args_schema: Type[BaseModel] = DestinationResearchInput

    def _run(self, destination: str, travel_style: str) -> str:
        # Simulated destination research - in production, this would call real APIs
        research_data = {
            "destination": destination,
            "travel_style": travel_style,
            "key_attractions": [
                "Historic landmarks and museums",
                "Local markets and food scenes",
                "Cultural districts and neighborhoods",
                "Natural attractions and parks"
            ],
            "cultural_tips": [
                "Local etiquette and customs",
                "Language basics and helpful phrases",
                "Tipping culture and payment methods",
                "Dress codes for religious sites"
            ],
            "seasonal_info": {
                "best_time_to_visit": "Depends on activities and weather preferences",
                "weather_patterns": "Research current seasonal conditions",
                "local_events": "Check for festivals and holidays during travel dates"
            },
            "transportation": {
                "getting_around": "Public transport, ride-sharing, walking options",
                "from_airport": "Airport transfer options and costs"
            }
        }
        
        return json.dumps(research_data, indent=2)


class FlightSearchTool(BaseTool):
    name: str = "Flight Search Tool"
    description: str = (
        "Search for flight options with pricing, schedules, and booking recommendations "
        "based on origin, destination, dates, and budget."
    )
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(self, origin: str, destination: str, departure_date: str, 
             return_date: str = None, budget_range: str = "") -> str:
        # Simulated flight search - in production, this would integrate with real flight APIs
        flight_options = {
            "search_criteria": {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "budget_range": budget_range
            },
            "recommendations": [
                {
                    "airline": "Sample Airline",
                    "price": "$650",
                    "duration": "14h 30m",
                    "stops": "1 stop",
                    "departure_time": "08:30",
                    "arrival_time": "16:00+1",
                    "booking_platform": "Airline direct or travel agency"
                },
                {
                    "airline": "Budget Carrier",
                    "price": "$480",
                    "duration": "18h 45m",
                    "stops": "2 stops",
                    "departure_time": "22:15",
                    "arrival_time": "19:30+1",
                    "booking_platform": "Compare on flight aggregators"
                }
            ],
            "booking_tips": [
                "Book 4-6 weeks in advance for best prices",
                "Consider nearby airports for potential savings",
                "Check airline websites directly for deals",
                "Be flexible with dates for lower fares"
            ]
        }
        
        return json.dumps(flight_options, indent=2)


class HotelSearchTool(BaseTool):
    name: str = "Hotel Search Tool"
    description: str = (
        "Search for accommodation options including hotels, hostels, and alternative "
        "lodging with pricing, amenities, and booking recommendations."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(self, destination: str, checkin_date: str, checkout_date: str,
             accommodation_type: str, budget_range: str) -> str:
        # Simulated hotel search - in production, this would integrate with booking APIs
        hotel_options = {
            "search_criteria": {
                "destination": destination,
                "checkin_date": checkin_date,
                "checkout_date": checkout_date,
                "accommodation_type": accommodation_type,
                "budget_range": budget_range
            },
            "recommendations": [
                {
                    "name": "Boutique City Hotel",
                    "type": "Boutique Hotel",
                    "price_per_night": "$120",
                    "rating": "4.2/5",
                    "amenities": ["Free WiFi", "Breakfast included", "Gym", "Central location"],
                    "booking_platforms": ["Hotel direct", "Booking.com", "Expedia"]
                },
                {
                    "name": "Modern Hostel",
                    "type": "Hostel",
                    "price_per_night": "$35",
                    "rating": "4.0/5",
                    "amenities": ["Free WiFi", "Kitchen access", "Social areas", "Lockers"],
                    "booking_platforms": ["Hostelworld", "Booking.com"]
                }
            ],
            "booking_tips": [
                "Check cancellation policies before booking",
                "Compare prices across multiple platforms",
                "Read recent reviews for current conditions",
                "Book refundable rates when possible"
            ]
        }
        
        return json.dumps(hotel_options, indent=2)


class ActivitySearchTool(BaseTool):
    name: str = "Activity Search Tool"
    description: str = (
        "Find activities, tours, and experiences based on traveler interests, "
        "travel style, and destination with pricing and booking information."
    )
    args_schema: Type[BaseModel] = ActivitySearchInput

    def _run(self, destination: str, interests: str, travel_style: str) -> str:
        # Simulated activity search - in production, this would integrate with activity APIs
        activities = {
            "search_criteria": {
                "destination": destination,
                "interests": interests,
                "travel_style": travel_style
            },
            "recommendations": [
                {
                    "name": "Cultural Walking Tour",
                    "type": "Guided Tour",
                    "duration": "3 hours",
                    "price": "$35",
                    "description": "Explore historic neighborhoods with local guide",
                    "booking_platforms": ["GetYourGuide", "Viator", "Local tour operators"]
                },
                {
                    "name": "Cooking Class Experience",
                    "type": "Cultural Activity",
                    "duration": "4 hours",
                    "price": "$85",
                    "description": "Learn to cook traditional dishes with local chef",
                    "booking_platforms": ["Airbnb Experiences", "Local cooking schools"]
                },
                {
                    "name": "Museum Pass",
                    "type": "Self-guided",
                    "duration": "Full day",
                    "price": "$45",
                    "description": "Access to multiple museums and cultural sites",
                    "booking_platforms": ["Official tourism website", "Museum websites"]
                }
            ],
            "local_tips": [
                "Book popular activities in advance",
                "Check for combo tickets and city passes",
                "Ask locals for hidden gem recommendations",
                "Consider free walking tours and activities"
            ]
        }
        
        return json.dumps(activities, indent=2)