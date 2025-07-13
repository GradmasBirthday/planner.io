from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from planner.tools.travel_tools import (
    DestinationResearchTool,
    FlightSearchTool,
    HotelSearchTool,
    ActivitySearchTool
)
from langchain_google_genai import ChatGoogleGenerativeAI
import os

@CrewBase
class Planner():
    """Voyagia Travel Planning Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Initialize Gemini LLM
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
            
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )

    @agent
    def trip_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['trip_planner'], # type: ignore[index]
            tools=[DestinationResearchTool(), ActivitySearchTool()],
            llm=self.llm,
            verbose=True
        )

    @agent
    def booking_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['booking_agent'], # type: ignore[index]
            tools=[FlightSearchTool(), HotelSearchTool()],
            llm=self.llm,
            verbose=True
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'], # type: ignore[index]
            tools=[DestinationResearchTool(), ActivitySearchTool()],
            llm=self.llm,
            verbose=True
        )

    @task
    def itinerary_planning(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_planning'], # type: ignore[index]
            agent=self.trip_planner()
        )

    @task
    def booking_research(self) -> Task:
        return Task(
            config=self.tasks_config['booking_research'], # type: ignore[index]
            agent=self.booking_agent()
        )

    @task
    def local_insights(self) -> Task:
        return Task(
            config=self.tasks_config['local_insights'], # type: ignore[index]
            agent=self.local_expert(),
            output_file='travel_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Voyagia Travel Planning crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
