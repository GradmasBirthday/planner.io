#!/usr/bin/env python3
"""
Test script for the local discovery API endpoint
"""

import requests
import json
import sys

def test_local_discovery_api():
    """Test the /api/v1/local/discover endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/v1/local/discover"
    
    # Test cases
    test_cases = [
        {
            "name": "Tokyo with cultural interests",
            "data": {
                "location": "Tokyo, Japan",
                "interests": ["museums", "temples", "cultural", "traditional"],
                "travel_dates": "March 2024",
                "budget": "$1000-2000"
            }
        },
        {
            "name": "Paris with art and landmarks",
            "data": {
                "location": "Paris, France",
                "interests": ["art", "landmarks", "museums", "architecture"],
                "travel_dates": None,
                "budget": None
            }
        },
        {
            "name": "New York with entertainment",
            "data": {
                "location": "New York, USA",
                "interests": ["entertainment", "theaters", "landmarks", "parks"],
                "travel_dates": "Summer 2024",
                "budget": "$2000-3000"
            }
        },
        {
            "name": "Unknown city (should use AI fallback)",
            "data": {
                "location": "Zurich, Switzerland",
                "interests": ["mountains", "lakes", "nature", "hiking"],
                "travel_dates": None,
                "budget": None
            }
        }
    ]
    
    print("Testing Local Discovery API Endpoint")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 30)
        
        try:
            # Make API request
            response = requests.post(url, json=test_case['data'], timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    discovery_data = data["data"]
                    
                    print(f"✅ SUCCESS: Found {discovery_data['total_results']} places")
                    print(f"Location: {discovery_data['location']}")
                    print(f"Interests: {', '.join(discovery_data['interests'])}")
                    
                    # Print some sample places
                    print("\nSample Places:")
                    for i, experience in enumerate(discovery_data['experiences'][:3]):
                        print(f"  {i+1}. {experience['name']}")
                        print(f"     Category: {experience['category']}")
                        print(f"     Rating: {experience.get('rating', 'N/A')}")
                        print(f"     Description: {experience['description'][:100]}...")
                        print()
                    
                    # Print restaurants
                    if discovery_data['restaurants']:
                        print(f"Restaurants found: {len(discovery_data['restaurants'])}")
                        for restaurant in discovery_data['restaurants'][:2]:
                            print(f"  - {restaurant['name']} ({restaurant.get('cuisine', 'Unknown')})")
                    
                    # Print attractions
                    if discovery_data['attractions']:
                        print(f"Attractions found: {len(discovery_data['attractions'])}")
                        for attraction in discovery_data['attractions'][:2]:
                            print(f"  - {attraction['name']} ({attraction.get('category', 'Unknown')})")
                    
                else:
                    print(f"❌ API ERROR: {data.get('message', 'Unknown error')}")
                    
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR: Could not connect to API server")
            print("Make sure the API server is running on localhost:8000")
            
        except requests.exceptions.Timeout:
            print("❌ TIMEOUT ERROR: Request took too long")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

def test_api_health():
    """Test if the API server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running")
        return False
    except Exception as e:
        print(f"❌ Error checking API health: {str(e)}")
        return False

if __name__ == "__main__":
    print("Local Discovery API Test")
    print("=" * 50)
    
    # Check if API server is running
    if not test_api_health():
        print("\nTo start the API server, run:")
        print("cd src/planner && python -m uvicorn travel_api:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    # Run the tests
    test_local_discovery_api() 