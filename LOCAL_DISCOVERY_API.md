# Local Discovery API

## Overview

The `/api/v1/local/discover` endpoint provides famous places, attractions, restaurants, and local experiences for any city worldwide. It's designed to return curated, high-quality recommendations based on user interests.

## Endpoint

```
POST /api/v1/local/discover
```

## Request Format

```json
{
  "location": "Tokyo, Japan",
  "interests": ["museums", "temples", "cultural", "traditional"],
  "travel_dates": "March 2024",
  "budget": "$1000-2000"
}
```

### Parameters

- **location** (required): City name with optional country (e.g., "Tokyo, Japan", "Paris", "New York, USA")
- **interests** (required): Array of interests to filter places by
- **travel_dates** (optional): Travel dates for context
- **budget** (optional): Budget range for recommendations

### Supported Interests

- **Culture & History**: `cultural`, `historical`, `museums`, `art`, `galleries`, `monuments`
- **Religious**: `religious`, `temples`, `churches`, `spiritual`, `meditation`
- **Nature**: `nature`, `parks`, `gardens`, `hiking`, `outdoor`, `scenic`
- **Architecture**: `architecture`, `landmarks`, `buildings`, `modern`, `traditional`
- **Food & Dining**: `food`, `restaurants`, `local cuisine`, `markets`, `street food`
- **Entertainment**: `entertainment`, `nightlife`, `theaters`, `music`, `shows`
- **Shopping**: `shopping`, `markets`, `boutiques`, `luxury`, `local products`
- **Sports & Activities**: `sports`, `activities`, `adventure`, `water sports`
- **Relaxation**: `relaxation`, `spa`, `wellness`, `peaceful`, `quiet`

## Response Format

```json
{
  "success": true,
  "message": "Local discovery completed successfully",
  "data": {
    "location": "Tokyo, Japan",
    "interests": ["museums", "temples", "cultural", "traditional"],
    "total_results": 8,
    "experiences": [
      {
        "name": "Senso-ji Temple",
        "description": "Tokyo's oldest temple, founded in 628 AD",
        "category": "religious",
        "location": "Tokyo, Japan",
        "price_range": "Free",
        "rating": 4.3,
        "opening_hours": "6:00-17:00",
        "booking_required": false,
        "contact_info": null,
        "why_recommended": "Most visited spiritual site in the world, iconic Tokyo landmark",
        "seasonal_info": null
      }
    ],
    "restaurants": [
      {
        "name": "Tsukiji Outer Market",
        "cuisine": "Local",
        "rating": 4.6,
        "price_range": "¥500-2,000",
        "location": "Tokyo, Japan"
      }
    ],
    "attractions": [
      {
        "name": "Tokyo National Museum",
        "category": "museum",
        "rating": 4.5,
        "description": "Japan's premier museum with extensive collection",
        "location": "Tokyo, Japan"
      }
    ],
    "events": [
      {
        "name": "Local Food Festival",
        "date": "This weekend",
        "location": "Tokyo, Japan"
      }
    ],
    "deals": [
      {
        "description": "10% off museum admissions",
        "discount": "10%",
        "expires": "End of month"
      }
    ]
  }
}
```

## Features

### 🌍 **Comprehensive City Coverage**
- **Major Cities**: Tokyo, Paris, London, New York, Barcelona, Rome, Amsterdam, Dubai, Sydney, Singapore, Bangkok
- **AI Fallback**: Uses Google Gemini AI for cities not in the database
- **Detailed Information**: Opening hours, ratings, prices, descriptions

### 🎯 **Smart Interest Matching**
- **Semantic Matching**: Finds places based on interest relevance
- **Category Filtering**: Automatically categorizes places by type
- **Personalized Results**: Prioritizes places matching user interests

### 🔄 **Intelligent Fallbacks**
- **Database First**: Uses curated data for major cities
- **AI Generation**: Generates places for unknown cities
- **Graceful Degradation**: Returns basic places if all else fails

### 📊 **Rich Data Structure**
- **Experiences**: Detailed place information with ratings and hours
- **Restaurants**: Cuisine type, price range, ratings
- **Attractions**: Category, descriptions, ratings
- **Events**: Local events and activities
- **Deals**: Current offers and discounts

## Example Requests

### Tokyo Cultural Experience
```bash
curl -X POST "http://localhost:8000/api/v1/local/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Tokyo, Japan",
    "interests": ["temples", "museums", "cultural", "traditional"],
    "travel_dates": "March 2024",
    "budget": "$1000-2000"
  }'
```

### Paris Art & Architecture
```bash
curl -X POST "http://localhost:8000/api/v1/local/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Paris, France",
    "interests": ["art", "museums", "architecture", "landmarks"]
  }'
```

### New York Entertainment
```bash
curl -X POST "http://localhost:8000/api/v1/local/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New York, USA",
    "interests": ["entertainment", "theaters", "broadway", "nightlife"],
    "budget": "$2000-3000"
  }'
```

## Error Handling

### 400 Bad Request
```json
{
  "success": false,
  "message": "Validation Error",
  "detail": [
    {
      "loc": ["interests"],
      "msg": "At least one interest is required",
      "type": "value_error"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error",
  "detail": "Service temporarily unavailable"
}
```

## Getting Started

### 1. Start the API Server
```bash
cd src/planner
python -m uvicorn travel_api:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test the API
```bash
python test_local_discovery_api.py
```

### 3. Use in Frontend
```javascript
const response = await fetch('/api/v1/local/discover', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    location: 'Tokyo, Japan',
    interests: ['museums', 'temples', 'cultural'],
    travel_dates: 'March 2024',
    budget: '$1000-2000'
  })
});

const data = await response.json();
if (data.success) {
  console.log(`Found ${data.data.total_results} places`);
  console.log(data.data.experiences);
}
```

## Architecture

```
Frontend Request
    ↓
Travel API (/api/v1/local/discover)
    ↓
TravelPlanningService.discover_local()
    ↓
LocalDiscoveryService.discover_places()
    ↓
┌─────────────────┬─────────────────┐
│   Database      │   AI Fallback   │
│   (Major Cities)│   (Gemini API)  │
└─────────────────┴─────────────────┘
    ↓
Structured Response (LocalDiscoveryData)
```

## Database Coverage

The API includes comprehensive data for these major cities:

- **Tokyo, Japan** - 10 famous places
- **Paris, France** - 10 famous places  
- **London, UK** - 10 famous places
- **New York, USA** - 10 famous places
- **Barcelona, Spain** - 8 famous places
- **Rome, Italy** - 8 famous places
- **Amsterdam, Netherlands** - 8 famous places
- **Dubai, UAE** - 8 famous places
- **Sydney, Australia** - 8 famous places
- **Singapore** - 8 famous places
- **Bangkok, Thailand** - 8 famous places

For cities not in the database, the API uses Google Gemini AI to generate relevant recommendations.

## Rate Limits

- **Development**: No rate limits
- **Production**: 100 requests per minute per IP (recommended)

## Dependencies

- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Google Gemini AI**: AI-powered place generation
- **asyncio**: Asynchronous processing

## Contributing

To add a new city to the database:

1. Add city data to `LocalDiscoveryService._load_places_database()`
2. Include at least 8-10 famous places
3. Ensure proper categorization and interests mapping
4. Test with the test script

## Support

For issues or questions, please check:
- API logs for error details
- Test script for debugging
- Ensure Google Gemini API key is configured for AI fallback 