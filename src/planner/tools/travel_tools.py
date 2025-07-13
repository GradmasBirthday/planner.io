from crewai.tools import BaseTool
from typing import Type, Dict, List, Optional
from pydantic import BaseModel, Field
import json
import os
import asyncio
import re
from datetime import datetime, timedelta
from exa_py import Exa
from dotenv import load_dotenv
from stagehand import Stagehand
from stagehand.schemas import ExtractOptions

load_dotenv()


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


class ContactInfo(BaseModel):
    """Contact information for a lodging."""
    email: Optional[str] = Field(None, description="Email address for the property")
    phone: Optional[str] = Field(None, description="Phone number for the property")
    website: Optional[str] = Field(None, description="Official website URL")
    
class LodgingInfo(BaseModel):
    """Data schema for scraped lodging information."""
    name: str = Field(description="The hostel or lodging name")
    description: Optional[str] = Field(None, description="Any details about the place")
    highlights: Optional[List[str]] = Field(default_factory=list, description="Key features or highlights mentioned")
    contact: Optional[ContactInfo] = Field(None, description="Contact information if available")
    address: Optional[str] = Field(None, description="Physical address of the property")


class LodgingList(BaseModel):
    """A list of lodging options found on a page."""
    lodgings: List[LodgingInfo] = Field(default_factory=list, description="List of lodging options found on the page")


def sanitize_url_for_filename(url: str) -> str:
    """Sanitizes a URL to be used as a valid filename."""
    # Remove protocol
    sanitized = re.sub(r'^https?:\/\/', '', url)
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9-]', '_', sanitized)
    # Truncate to a reasonable length to avoid OS limits
    return sanitized[:100]


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
        "Search for accommodation options. For standard hotels, it uses booking APIs. "
        "For niche options like hostels and guesthouses, it scrapes specialty websites and blogs to find unique, budget-friendly lodging."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(self, destination: str, accommodation_type: str, budget_range: str) -> str:
        return asyncio.run(self._arun(
            destination=destination,
            accommodation_type=accommodation_type,
            budget_range=budget_range
        ))

    async def _arun(self, destination: str, accommodation_type: str, budget_range: str) -> str:
        """Asynchronously scrapes the web for niche lodging options."""
        print(f"--- Scraping for {accommodation_type} in {destination} ---")
        
        # Step 1: Use Exa to find promising websites (blogs, guides, etc.)
        exa_query = f"best budget-friendly {accommodation_type} in {destination} with reviews for {budget_range} price range"
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        try:
            print(f"Finding sources with Exa for query: {exa_query}")
            search_response = exa.search_and_contents(
                exa_query, 
                num_results=3,
                include_domains=["thebrokebackpacker.com", "nomadicmatt.com", "gobackpacking.com", "travelfreak.com"],
            )
            urls = [res.url for res in search_response.results]
            if not urls:
                return "Could not find any relevant sources for niche lodging."
            print(f"Found {len(urls)} sources to scrape: {urls}")

        except Exception as e:
            return f"An error occurred during Exa search: {e}"

        # Step 2: Use Stagehand to scrape each URL for lodging details
        sh = None
        all_lodging_options = []
        try:
            cache_dir = "cached_results"
            os.makedirs(cache_dir, exist_ok=True)

            sh = Stagehand(
                browserbase_api_key=os.getenv("BROWSERBASE_API_KEY"),
                browserbase_project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
                model_api_key=os.getenv("OPENAI_API_KEY"),
                model_name="openai/gpt-3.5-turbo"
            )
            await sh.init()
            p = sh.page

            for url in urls:
                sanitized_url = sanitize_url_for_filename(url)
                cache_filepath = os.path.join(cache_dir, f"{sanitized_url}.json")

                if os.path.exists(cache_filepath):
                    with open(cache_filepath, "r") as f:
                        cached_data = json.load(f)
                        
                        # Check if this URL was blacklisted
                        if isinstance(cached_data, dict) and cached_data.get("blacklisted"):
                            blacklist_time = datetime.fromisoformat(cached_data["timestamp"])
                            # Check if blacklist has expired (30 days)
                            if datetime.now() - blacklist_time < timedelta(days=30):
                                print(f"Skipping blacklisted URL (reason: {cached_data['reason']}): {url}")
                                print(f"Will retry after {blacklist_time + timedelta(days=30)}")
                                continue
                            else:
                                print(f"Blacklist expired for {url}, attempting to scrape again...")
                        else:
                            # Normal cache expiration check (7 days)
                            file_mod_time = datetime.fromtimestamp(os.path.getmtime(cache_filepath))
                            if datetime.now() - file_mod_time < timedelta(days=7):
                                print(f"Loading fresh cached results for {url}...")
                                lodgings_data = cached_data if isinstance(cached_data, list) else cached_data.get("lodgings", [])
                                for item in lodgings_data:
                                    all_lodging_options.append(LodgingInfo(**item))
                                continue
                            else:
                                print(f"Cache for {url} is stale (over 1 week old). Re-scraping...")

                print(f"Scraping {url}...")
                await p.goto(url, timeout=60000)  # Increase timeout to 60 seconds
                await p.wait_for_load_state("domcontentloaded", timeout=60000)
                # Wait a bit for any JavaScript to run
                await asyncio.sleep(2)

                try:
                    # First try to find and focus on the main content area
                    await p.act("Find and click the main article content or list of hostels")
                    
                    # Try extraction with focused viewport
                    lodging_list = await p.extract(
                        ExtractOptions(
                            instruction="""
                            Look through this travel blog post and find mentions of hostels or lodgings.
                            For each place mentioned:
                            1. Get the name - this is required
                            2. Include any descriptive text as the description
                            3. List any standout features or highlights
                            4. Look for contact information (email, phone, website)
                            5. Note the physical address if mentioned
                            
                            Pay special attention to any contact sections, footer areas, 
                            or "Contact Us" links that might contain email addresses or phone numbers.
                            """,
                            schema_definition=LodgingList,
                            screenshot_of_visible_portion=True,
                            max_tokens=8000
                        )
                    )

                    # Second pass: For each lodging with a website, visit it to get contact info
                    if lodging_list and lodging_list.lodgings:
                        for lodging in lodging_list.lodgings:
                            try:
                                if lodging.contact and lodging.contact.website:
                                    print(f"Checking official website for {lodging.name}...")
                                    await p.goto(lodging.contact.website, timeout=60000)
                                    await p.wait_for_load_state("domcontentloaded", timeout=60000)
                                    
                                    contact_info = await p.extract(
                                        ExtractOptions(
                                            instruction="Find the property's contact information (email, phone) from their official website.",
                                            schema_definition=ContactInfo,
                                            screenshot_of_visible_portion=True,
                                            max_tokens=4000
                                        )
                                    )
                                    if contact_info:
                                        lodging.contact = contact_info
                            except Exception as e:
                                print(f"Error getting contact info for {lodging.name}: {str(e)}")
                                continue

                    if lodging_list and lodging_list.lodgings:
                        # Store successful results with timestamp
                        cache_data = {
                            "blacklisted": False,
                            "timestamp": datetime.now().isoformat(),
                            "lodgings": [lodging.dict() for lodging in lodging_list.lodgings]
                        }
                        with open(cache_filepath, "w") as f:
                            json.dump(cache_data, f, indent=2)
                        print(f"Saved formatted results to cache: {cache_filepath}")
                        all_lodging_options.extend(lodging_list.lodgings)
                    else:
                        print(f"Could not extract lodging information from {url}")

                except Exception as e:
                    error_str = str(e)
                    print(f"Error processing {url}: {error_str}")
                    
                    # Check if the error is token-related
                    if "maximum context length" in error_str.lower() or "token" in error_str.lower():
                        print(f"URL exceeded token limits. Blacklisting for 30 days: {url}")
                        # Cache empty results with blacklist info
                        blacklist_data = {
                            "blacklisted": True,
                            "reason": "Token limit exceeded",
                            "timestamp": datetime.now().isoformat(),
                            "retry_after": (datetime.now() + timedelta(days=30)).isoformat(),
                            "lodgings": []
                        }
                        with open(cache_filepath, "w") as f:
                            json.dump(blacklist_data, f, indent=2)
                    
                    continue  # Skip to next URL on error
            
            return json.dumps([opt.dict() for opt in all_lodging_options], indent=2)

        except Exception as e:
            return f"An error occurred during web scraping: {e}"
        finally:
            if sh:
                await sh.close()


class ActivitySearchTool(BaseTool):
    name: str = "Activity Search Tool"
    description: str = (
        "Find activities, tours, and experiences based on traveler interests, "
        "travel style, and destination with pricing and booking information."
    )
    args_schema: Type[BaseModel] = ActivitySearchInput

    def _run(self, destination: str, interests: str, travel_style: str) -> str:
        return asyncio.run(
            self._arun(
                destination=destination, interests=interests, travel_style=travel_style
            )
        )

    async def _arun(self, destination: str, interests: str, travel_style: str) -> str:
        """Asynchronously find activities using Exa."""
        query = f"Best activities and tours in {destination} for a traveler interested in {interests} with a {travel_style} travel style."
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        try:
            search_response = await exa.asearch_and_get_contents(
                query,
                num_results=5,
                text={"max_characters": 1000},
                highlights=True,
            )

            results = [
                {
                    "title": res.title,
                    "url": res.url,
                    "content": res.text,
                    "highlights": res.highlights,
                }
                for res in search_response.results
            ]
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"An error occurred during activity search: {e}"

if __name__ == "__main__":
    tool = HotelSearchTool()
    print(tool.run("Tokyo", "hostel", "$100"))