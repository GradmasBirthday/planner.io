#!/usr/bin/env python3
"""
Test CrewAI compatibility with Gemini using the official CrewAI LLM wrapper, per Google AI documentation.
"""
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import LLM, Agent, Task, Crew, Process

# Set up Gemini LLM using CrewAI's built-in wrapper
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ No GEMINI_API_KEY found - please set it in your environment.")
    exit(1)

gemini_llm = LLM(
    model="gemini/gemini-2.5-pro",  # Use the official Gemini 2.5 Pro model
    api_key=GEMINI_API_KEY,
    temperature=0.0
)

# Define a simple agent
agent = Agent(
    role="Travel Planner",
    goal="Create simple travel recommendations",
    backstory="You are a helpful travel assistant.",
    verbose=True,
    llm=gemini_llm
)

# Define a simple task
travel_task = Task(
    description="Suggest 3 must-visit places in Paris.",
    expected_output="A list of 3 places.",
    agent=agent
)

# Set up the crew
crew = Crew(
    agents=[agent],
    tasks=[travel_task],
    process=Process.sequential,
    verbose=True
)

def test_crewai_with_gemini():
    print("\n=== Testing CrewAI with Gemini LLM (Official Integration) ===")
    try:
        result = crew.kickoff()
        print(f"✅ CrewAI + Gemini Success: {result}")
        return True
    except Exception as e:
        print(f"❌ CrewAI + Gemini Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing CrewAI with Gemini (official integration)...\n")
    test_crewai_with_gemini()