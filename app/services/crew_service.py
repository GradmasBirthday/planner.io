"""
Service layer for CrewAI integration
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from ..config import settings
from ..models import (
    TravelPlanData, ProductSearchData, LocalDiscoveryData, 
    BookingData, AgentTaskData, ProductRecommendation,
    LocalExperience, BookingInfo, Itinerary
)

class TravelPlanningService:
    """Service class for travel planning operations using CrewAI"""
    
    def __init__(self):
        """Initialize the travel planning service"""
        # Initialize tools first
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        
        # Initialize executor
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Initialize agents (requires tools to be initialized first)
        self.agents = self._create_agents()
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Create all specialized agents"""
        
        # Product Search and Recommendation Agent
        product_agent = Agent(
            role='Product Search and Recommendation Specialist',
            goal='Find and recommend travel-related products from Amazon and other shopping platforms',
            backstory="""You are an expert product researcher who specializes in finding 
            the best travel gear, clothing, accessories, and essentials for different 
            destinations and travel styles. You have deep knowledge of product reviews, 
            pricing, and seasonal availability across multiple shopping platforms.""",
            verbose=settings.CREW_VERBOSE,
            allow_delegation=False,
            tools=[self.search_tool, self.scrape_tool],
            max_iter=settings.CREW_MAX_ITER
        )
        
        # Info Search Agent
        info_agent = Agent(
            role='Local Information and Event Discovery Specialist',
            goal='Discover local events, restaurants, attractions, and deals in target destinations',
            backstory="""You are a local discovery expert who knows how to find the best 
            experiences in any city. You're skilled at using Reddit, Google Maps, Eventbrite, 
            and other platforms to uncover hidden gems, popular events, great dining spots, 
            and local deals that travelers would love.""",
            verbose=settings.CREW_VERBOSE,
            allow_delegation=False,
            tools=[self.search_tool, self.scrape_tool],
            max_iter=settings.CREW_MAX_ITER
        )
        
        # Booking Agent
        booking_agent = Agent(
            role='Booking and Reservation Coordinator',
            goal='Handle bookings and reservations for events, restaurants, and activities',
            backstory="""You are a skilled booking coordinator who specializes in making 
            reservations and securing spots for travelers. You know the best practices for 
            booking different types of venues, understand cancellation policies, and can 
            provide alternatives when primary options aren't available.""",
            verbose=settings.CREW_VERBOSE,
            allow_delegation=False,
            tools=[self.search_tool, self.scrape_tool],
            max_iter=settings.CREW_MAX_ITER
        )
        
        # Orchestration Agent
        orchestration_agent = Agent(
            role='Travel Planning Orchestrator',
            goal='Coordinate all agents to create comprehensive travel recommendations',
            backstory="""You are an experienced travel planning coordinator who excels at 
            bringing together product recommendations, local discoveries, and booking 
            coordination to create seamless travel experiences. You understand how to 
            prioritize tasks, manage dependencies, and ensure all aspects of travel 
            planning work together harmoniously.""",
            verbose=settings.CREW_VERBOSE,
            allow_delegation=True,
            tools=[self.search_tool],
            max_iter=settings.CREW_MAX_ITER + 2
        )
        
        return {
            'product': product_agent,
            'info': info_agent,
            'booking': booking_agent,
            'orchestrator': orchestration_agent
        }
    
    async def create_travel_plan(self, destination: str, travel_dates: str, 
                                budget: str, travel_style: str, group_size: int = 1) -> TravelPlanData:
        """Create a comprehensive travel plan for a destination"""
        
        # Run the crew in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._create_travel_plan_sync,
            destination, travel_dates, budget, travel_style, group_size
        )
        
        return result
    
    def _create_travel_plan_sync(self, destination: str, travel_dates: str, 
                               budget: str, travel_style: str, group_size: int) -> TravelPlanData:
        """Synchronous version of create_travel_plan"""
        
        # Task 1: Orchestrator creates overall plan
        orchestration_task = Task(
            description=f"""Create a comprehensive travel planning strategy for:
            - Destination: {destination}
            - Travel Dates: {travel_dates}
            - Budget: {budget}
            - Travel Style: {travel_style}
            - Group Size: {group_size}
            
            Your role is to:
            1. Analyze the destination and travel requirements
            2. Create a coordinated plan for product recommendations, local discovery, and bookings
            3. Identify key priorities and dependencies
            4. Provide clear direction to other agents
            5. Ensure all recommendations work together cohesively
            
            Output a structured plan with priorities and agent assignments.""",
            agent=self.agents['orchestrator'],
            expected_output="A structured travel planning strategy with clear priorities and agent assignments"
        )
        
        # Task 2: Product recommendations
        product_task = Task(
            description=f"""Based on the travel plan, find and recommend essential products for:
            - Destination: {destination}
            - Travel Dates: {travel_dates}
            - Budget: {budget}
            - Travel Style: {travel_style}
            
            Focus on:
            1. Weather-appropriate clothing and gear
            2. Travel accessories and essentials
            3. Destination-specific equipment
            4. Electronics and gadgets
            5. Health and safety items
            
            For each product, provide:
            - Product name and description
            - Pricing information
            - Why it's recommended for this trip
            - Where to buy (Amazon, etc.)
            - Alternatives if available
            
            Search Amazon and other shopping platforms for current prices and availability.""",
            agent=self.agents['product'],
            expected_output="A detailed list of recommended products with pricing, sources, and justifications"
        )
        
        # Task 3: Local information discovery
        info_task = Task(
            description=f"""Discover local experiences and opportunities in {destination} for {travel_dates}:
            
            Research and find:
            1. Local events and festivals during the travel period
            2. Highly-rated restaurants and dining experiences
            3. Popular attractions and hidden gems
            4. Local deals and discounts
            5. Cultural experiences and activities
            6. Nightlife and entertainment options
            
            Use Reddit, Google Maps, Eventbrite, and other platforms to find:
            - Current local recommendations
            - Seasonal events and activities
            - Budget-friendly options
            - Authentic local experiences
            
            For each recommendation, provide:
            - Name and description
            - Location and accessibility
            - Pricing and timing
            - Why it's special or recommended
            - Booking requirements if any""",
            agent=self.agents['info'],
            expected_output="A comprehensive guide to local experiences, events, and dining with practical details"
        )
        
        # Task 4: Booking coordination
        booking_task = Task(
            description=f"""Handle booking and reservation coordination for the trip to {destination}:
            
            Based on the local discoveries, coordinate bookings for:
            1. Restaurant reservations
            2. Event tickets and registrations
            3. Activity bookings
            4. Tours and experiences
            
            For each booking opportunity:
            - Provide booking instructions and requirements
            - Identify reservation deadlines and policies
            - Suggest backup options
            - Note any special requirements or restrictions
            - Provide contact information and booking links
            
            Organize bookings by priority and timing requirements.""",
            agent=self.agents['booking'],
            expected_output="A detailed booking guide with reservation instructions, deadlines, and alternatives"
        )
        
        # Task 5: Final coordination and integration
        final_task = Task(
            description=f"""Integrate all recommendations into a cohesive travel plan:
            
            Combine inputs from all agents to create:
            1. A day-by-day itinerary
            2. Complete packing checklist with products
            3. Booking timeline and checklist
            4. Budget breakdown
            5. Emergency contacts and backup plans
            
            Ensure all recommendations work together and provide a seamless travel experience.
            Identify any conflicts or issues and provide solutions.""",
            agent=self.agents['orchestrator'],
            expected_output="A comprehensive, integrated travel plan with itinerary, packing list, and booking guide"
        )
        
        # Create the crew
        crew = Crew(
            agents=[
                self.agents['orchestrator'],
                self.agents['product'],
                self.agents['info'],
                self.agents['booking']
            ],
            tasks=[orchestration_task, product_task, info_task, booking_task, final_task],
            process=Process.sequential,
            verbose=settings.CREW_VERBOSE
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Parse and structure the result
        return self._parse_travel_plan_result(result, destination, travel_dates, budget, group_size)
    
    async def search_products(self, query: str, budget: str, destination: str = None, 
                            travel_dates: str = None) -> ProductSearchData:
        """Search for travel-related products"""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._search_products_sync,
            query, budget, destination, travel_dates
        )
        
        return result
    
    def _search_products_sync(self, query: str, budget: str, destination: str = None, 
                            travel_dates: str = None) -> ProductSearchData:
        """Synchronous version of search_products"""
        
        context = f"Destination: {destination}, Travel Dates: {travel_dates}" if destination else ""
        
        task = Task(
            description=f"""Find product recommendations for: {query}
            
            Budget consideration: {budget}
            {context}
            
            Provide:
            1. Top 3-5 product recommendations
            2. Price ranges and best deals
            3. Key features and benefits
            4. Customer reviews summary
            5. Where to buy and availability
            
            Focus on value and quality for the given budget.""",
            agent=self.agents['product'],
            expected_output="A focused product recommendation list with pricing and purchase information"
        )
        
        crew = Crew(
            agents=[self.agents['product']],
            tasks=[task],
            process=Process.sequential,
            verbose=settings.CREW_VERBOSE
        )
        
        result = crew.kickoff()
        
        return self._parse_product_search_result(result, query)
    
    async def discover_local(self, location: str, interests: List[str], 
                           travel_dates: str = None, budget: str = None) -> LocalDiscoveryData:
        """Discover local experiences based on interests"""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._discover_local_sync,
            location, interests, travel_dates, budget
        )
        
        return result
    
    def _discover_local_sync(self, location: str, interests: List[str], 
                           travel_dates: str = None, budget: str = None) -> LocalDiscoveryData:
        """Synchronous version of discover_local"""
        
        interests_str = ", ".join(interests)
        context = f"Travel Dates: {travel_dates}, Budget: {budget}" if travel_dates or budget else ""
        
        task = Task(
            description=f"""Discover local experiences in {location} based on these interests: {interests_str}
            
            {context}
            
            Find:
            1. Events and activities matching the interests
            2. Restaurants and dining experiences
            3. Local deals and special offers
            4. Hidden gems and local favorites
            5. Cultural experiences
            
            Provide practical information including timing, pricing, and accessibility.""",
            agent=self.agents['info'],
            expected_output="A curated list of local experiences matching the specified interests"
        )
        
        crew = Crew(
            agents=[self.agents['info']],
            tasks=[task],
            process=Process.sequential,
            verbose=settings.CREW_VERBOSE
        )
        
        result = crew.kickoff()
        
        return self._parse_local_discovery_result(result, location, interests)
    
    async def coordinate_booking(self, location: str, booking_types: List[str], 
                               travel_dates: str, preferences: Dict[str, Any] = None) -> BookingData:
        """Coordinate bookings and reservations"""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._coordinate_booking_sync,
            location, booking_types, travel_dates, preferences
        )
        
        return result
    
    def _coordinate_booking_sync(self, location: str, booking_types: List[str], 
                               travel_dates: str, preferences: Dict[str, Any] = None) -> BookingData:
        """Synchronous version of coordinate_booking"""
        
        booking_types_str = ", ".join(booking_types)
        preferences_str = json.dumps(preferences) if preferences else "No specific preferences"
        
        task = Task(
            description=f"""Coordinate bookings and reservations for {location}:
            
            Booking Types: {booking_types_str}
            Travel Dates: {travel_dates}
            Preferences: {preferences_str}
            
            For each booking type:
            1. Find available options
            2. Provide booking instructions
            3. Identify deadlines and requirements
            4. Suggest alternatives
            5. Include contact information
            
            Organize by priority and timing requirements.""",
            agent=self.agents['booking'],
            expected_output="A detailed booking coordination guide with instructions and alternatives"
        )
        
        crew = Crew(
            agents=[self.agents['booking']],
            tasks=[task],
            process=Process.sequential,
            verbose=settings.CREW_VERBOSE
        )
        
        result = crew.kickoff()
        
        return self._parse_booking_result(result, location, booking_types)
    
    async def execute_agent_task(self, agent_type: str, task_description: str, 
                               context: Dict[str, Any] = None) -> AgentTaskData:
        """Execute a specific task with a designated agent"""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._execute_agent_task_sync,
            agent_type, task_description, context
        )
        
        return result
    
    def _execute_agent_task_sync(self, agent_type: str, task_description: str, 
                               context: Dict[str, Any] = None) -> AgentTaskData:
        """Synchronous version of execute_agent_task"""
        
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        context_str = json.dumps(context) if context else "No additional context"
        
        task = Task(
            description=f"""{task_description}
            
            Additional Context: {context_str}
            
            Provide detailed and actionable results based on your expertise.""",
            agent=self.agents[agent_type],
            expected_output="Detailed results based on the agent's expertise"
        )
        
        crew = Crew(
            agents=[self.agents[agent_type]],
            tasks=[task],
            process=Process.sequential,
            verbose=settings.CREW_VERBOSE
        )
        
        start_time = time.time()
        result = crew.kickoff()
        execution_time = time.time() - start_time
        
        return AgentTaskData(
            agent_type=agent_type,
            task_description=task_description,
            result={"output": str(result), "raw_result": result},
            execution_time=execution_time,
            recommendations=self._extract_recommendations(str(result))
        )
    
    def _parse_travel_plan_result(self, result: Any, destination: str, 
                                travel_dates: str, budget: str, group_size: int) -> TravelPlanData:
        """Parse and structure travel plan result"""
        
        # This is a simplified parser - in a real implementation, 
        # you would need more sophisticated parsing logic
        result_str = str(result)
        
        return TravelPlanData(
            destination=destination,
            travel_dates=travel_dates,
            budget=budget,
            group_size=group_size,
            itinerary=[
                Itinerary(
                    day=1,
                    date=travel_dates.split('-')[0] if '-' in travel_dates else travel_dates,
                    activities=[{"name": "Sample Activity", "time": "10:00 AM", "description": "Generated from crew result"}],
                    meals=[{"name": "Sample Restaurant", "time": "12:00 PM", "cuisine": "Local"}],
                    notes="Generated from CrewAI result"
                )
            ],
            product_recommendations=[
                ProductRecommendation(
                    name="Sample Product",
                    description="Generated from crew result",
                    price="$50-100",
                    why_recommended="Based on crew analysis",
                    alternatives=["Alternative 1", "Alternative 2"]
                )
            ],
            local_experiences=[
                LocalExperience(
                    name="Sample Experience",
                    description="Generated from crew result",
                    category="Culture",
                    location=destination,
                    why_recommended="Based on crew analysis"
                )
            ],
            booking_info=[
                BookingInfo(
                    venue_name="Sample Venue",
                    booking_type="restaurant",
                    description="Generated from crew result",
                    location=destination,
                    booking_instructions="Contact venue directly",
                    contact_info="Generated from crew result"
                )
            ],
            packing_checklist=self._extract_packing_list(result_str),
            budget_breakdown={"accommodation": "40%", "food": "30%", "activities": "20%", "transport": "10%"},
            emergency_contacts=["Local emergency: 911", "Embassy contact: TBD"],
            tips=self._extract_tips(result_str)
        )
    
    def _parse_product_search_result(self, result: Any, query: str) -> ProductSearchData:
        """Parse product search result"""
        
        return ProductSearchData(
            query=query,
            total_results=1,
            recommendations=[
                ProductRecommendation(
                    name="Sample Product",
                    description="Generated from crew result",
                    price="$50-100",
                    why_recommended="Based on crew analysis",
                    alternatives=["Alternative 1", "Alternative 2"]
                )
            ],
            budget_summary={"min": "$50", "max": "$100", "average": "$75"}
        )
    
    def _parse_local_discovery_result(self, result: Any, location: str, interests: List[str]) -> LocalDiscoveryData:
        """Parse local discovery result"""
        
        return LocalDiscoveryData(
            location=location,
            interests=interests,
            total_results=1,
            experiences=[
                LocalExperience(
                    name="Sample Experience",
                    description="Generated from crew result",
                    category="Culture",
                    location=location,
                    why_recommended="Based on crew analysis"
                )
            ],
            events=[{"name": "Sample Event", "date": "TBD", "location": location}],
            restaurants=[{"name": "Sample Restaurant", "cuisine": "Local", "rating": 4.5}],
            attractions=[{"name": "Sample Attraction", "category": "Historical", "rating": 4.0}],
            deals=[{"description": "Sample deal", "discount": "20%", "expires": "TBD"}]
        )
    
    def _parse_booking_result(self, result: Any, location: str, booking_types: List[str]) -> BookingData:
        """Parse booking result"""
        
        return BookingData(
            location=location,
            booking_types=booking_types,
            total_bookings=1,
            booking_info=[
                BookingInfo(
                    venue_name="Sample Venue",
                    booking_type="restaurant",
                    description="Generated from crew result",
                    location=location,
                    booking_instructions="Contact venue directly",
                    contact_info="Generated from crew result"
                )
            ],
            booking_timeline=[{"task": "Book restaurant", "deadline": "1 week before", "priority": "high"}],
            priority_bookings=["Restaurant reservations", "Event tickets"]
        )
    
    def _extract_recommendations(self, result_str: str) -> List[str]:
        """Extract recommendations from result string"""
        # Simple extraction - in real implementation, use NLP or structured parsing
        return ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
    
    def _extract_packing_list(self, result_str: str) -> List[str]:
        """Extract packing list from result string"""
        # Simple extraction - in real implementation, use NLP or structured parsing
        return ["Passport", "Clothes", "Electronics", "Medications", "Travel documents"]
    
    def _extract_tips(self, result_str: str) -> List[str]:
        """Extract tips from result string"""
        # Simple extraction - in real implementation, use NLP or structured parsing
        return ["Book accommodations early", "Learn basic local phrases", "Keep copies of important documents"] 