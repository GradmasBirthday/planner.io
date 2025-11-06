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
            cache_dir = "cached_results/hotels"
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


class ActivityInfo(BaseModel):
    """Data schema for unique, non-touristy activities."""
    name: str = Field(description="Name or title of the activity")
    description: Optional[str] = Field(None, description="Detailed description of what it involves")
    location: Optional[str] = Field(None, description="Where to find it, possibly with directions")

class ActivityList(BaseModel):
    """A list of unique activities found."""
    activities: List[ActivityInfo] = Field(default_factory=list, description="List of activities found")

class ActivitySearchInput(BaseModel):
    """Input schema for activity search."""
    destination: str = Field(..., description="Destination city/area to search for activities")
    interests: str = Field(..., description="Type of activities interested in (e.g., 'food, art, nature')")
    travel_style: str = Field(..., description="Travel style (adventure, cultural, budget, etc.)")

class ActivitySearchTool(BaseTool):
    name: str = "Activity Search Tool"
    description: str = (
        "Find unique, non-touristy activities and experiences that locals love. "
        "Focuses on hidden gems, authentic experiences, and places off the beaten path."
    )
    args_schema: Type[BaseModel] = ActivitySearchInput

    def _run(self, destination: str, interests: str, travel_style: str) -> str:
        return asyncio.run(
            self._arun(
                destination=destination, interests=interests, travel_style=travel_style
            )
        )

    async def _arun(self, destination: str, interests: str, travel_style: str) -> str:
        """Asynchronously scrapes the web for unique, local activities."""
        print(f"--- Finding hidden gems in {destination} for {interests} interests ---")
        
        # Initialize Exa client
        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        
        # Step 1: Generate targeted search queries and find sources
        all_activities = []
        cache_dir = "cached_results/activities"
        os.makedirs(cache_dir, exist_ok=True)
        
        try:
            # First get our sources using Exa
            print("Finding sources with Exa...")
            search_response = exa.search_and_contents(  # Remove await here
                f"unique local activities hidden gems {destination} {interests} {travel_style}",
                num_results=3,
                include_domains=[
                    "reddit.com/",
                    "atlasobscura.com",
                    "culturalfoodies.com"
                ],
            )
            
            urls = [res.url for res in search_response.results]
            if not urls:
                return "Could not find any relevant sources for activities."
            print(f"Found {len(urls)} sources to scrape: {urls}")

            # Initialize Stagehand for scraping
            sh = Stagehand(
                browserbase_api_key=os.getenv("BROWSERBASE_API_KEY"),
                browserbase_project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
                model_api_key=os.getenv("OPENAI_API_KEY"),
                model_name="openai/gpt-3.5-turbo"
            )
            await sh.init()
            p = sh.page

            # Process each URL
            for url in urls:
                sanitized_url = sanitize_url_for_filename(url)
                cache_filepath = os.path.join(cache_dir, f"{sanitized_url}.json")
                
                # Check cache
                if os.path.exists(cache_filepath):
                    with open(cache_filepath, "r") as f:
                        cached_data = json.load(f)
                        
                        # Handle blacklisted URLs
                        if isinstance(cached_data, dict) and cached_data.get("blacklisted"):
                            blacklist_time = datetime.fromisoformat(cached_data["timestamp"])
                            if datetime.now() - blacklist_time < timedelta(days=30):
                                print(f"Skipping blacklisted URL: {url}")
                                continue
                        
                        # Handle valid cache
                        file_mod_time = datetime.fromtimestamp(os.path.getmtime(cache_filepath))
                        if datetime.now() - file_mod_time < timedelta(days=7):
                            print(f"Loading cached results for {url}")
                            activities_data = cached_data.get("activities", [])
                            for item in activities_data:
                                all_activities.append(ActivityInfo(**item))
                            continue
                
                print(f"Scraping {url}...")
                try:
                    await p.goto(url, timeout=60000)
                    await p.wait_for_load_state("domcontentloaded", timeout=60000)
                    await asyncio.sleep(2)
                    
                    # Try to find and focus on main content
                    await p.act("Find and focus on the main article or content area")
                    
                    # Extract activities
                    activity_list = await p.extract(
                        ExtractOptions(
                            instruction="""
                            Find unique, non-touristy activities and experiences mentioned in this content.
                            Focus on:
                            1. Hidden gems and local favorites
                            2. Specific locations and how to find them
                            3. Tips from locals or experienced travelers
                            4. Best times to visit
                            5. Cost information if available
                            
                            Ignore obvious tourist attractions and commercial tour offerings.
                            Rate authenticity based on how local/unique vs touristy it seems (1-10).
                            """,
                            schema_definition=ActivityList,
                            screenshot_of_visible_portion=True,
                            max_tokens=8000
                        )
                    )
                    
                    if activity_list and activity_list.activities:
                        # Store successful results
                        cache_data = {
                            "timestamp": datetime.now().isoformat(),
                            "activities": [activity.dict() for activity in activity_list.activities]
                        }
                        with open(cache_filepath, "w") as f:
                            json.dump(cache_data, f, indent=2)
                        all_activities.extend(activity_list.activities)
                    
                except Exception as e:
                    error_str = str(e)
                    print(f"Error processing {url}: {error_str}")
                    
                    if "maximum context length" in error_str.lower():
                        # Blacklist oversized pages
                        blacklist_data = {
                            "blacklisted": True,
                            "reason": "Token limit exceeded",
                            "timestamp": datetime.now().isoformat()
                        }
                        with open(cache_filepath, "w") as f:
                            json.dump(blacklist_data, f, indent=2)
                    continue

                            # Just filter duplicates
            filtered_activities = []
            seen_names = set()
            
            for activity in all_activities:
                if activity.name.lower() in seen_names:
                    continue
                filtered_activities.append(activity)
                seen_names.add(activity.name.lower())
            
            return json.dumps(
                [activity.dict() for activity in filtered_activities],
                indent=2
            )
            

        except Exception as e:
            return f"An error occurred during activity search: {e}"
        finally:
            if 'sh' in locals():
                await sh.close()

if __name__ == "__main__":
    tool = ActivitySearchTool()
    print(tool.run("Tokyo", "food", "adventure"))
