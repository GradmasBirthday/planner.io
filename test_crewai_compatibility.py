#!/usr/bin/env python3
"""
Test CrewAI compatibility with different LLMs
"""
from dotenv import load_dotenv
load_dotenv()

import os
from crewai import Agent, Task, Crew

def test_crewai_with_default():
    """Test CrewAI with default LLM (OpenAI)"""
    print("=== Testing CrewAI with Default LLM ===")
    try:
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ No OPENAI_API_KEY found - skipping OpenAI test")
            return False
            
        agent = Agent(
            role="Travel Planner",
            goal="Create simple travel recommendations",
            backstory="You are a helpful travel assistant.",
            verbose=True
        )
        
        task = Task(
            description="Suggest 3 must-visit places in Paris.",
            expected_output="A list of 3 places.",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        print(f"✅ OpenAI Success: {result}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return False

def test_crewai_with_gemini():
    """Test CrewAI with Gemini LLM"""
    print("\n=== Testing CrewAI with Gemini LLM ===")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        if not os.getenv("GOOGLE_API_KEY"):
            print("❌ No GOOGLE_API_KEY found - skipping Gemini test")
            return False
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        agent = Agent(
            role="Travel Planner",
            goal="Create simple travel recommendations",
            backstory="You are a helpful travel assistant.",
            llm=llm,
            verbose=True
        )
        
        task = Task(
            description="Suggest 3 must-visit places in Paris.",
            expected_output="A list of 3 places.",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        print(f"✅ Gemini Success: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gemini_standalone():
    """Test Gemini without CrewAI"""
    print("\n=== Testing Gemini Standalone ===")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        response = llm.invoke("Suggest 3 must-visit places in Paris for a cultural traveler.")
        print(f"✅ Gemini Standalone Success: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini Standalone Error: {e}")
        return False

def check_crewai_llm_wrapper():
    """Check how CrewAI wraps LLMs"""
    print("\n=== Checking CrewAI LLM Wrapper ===")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from crewai.llm import LLM as CrewLLM
        
        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        # Check if CrewAI wraps the LLM
        print(f"Gemini LLM type: {type(gemini_llm)}")
        print(f"Gemini LLM has 'call' method: {hasattr(gemini_llm, 'call')}")
        print(f"Gemini LLM has 'invoke' method: {hasattr(gemini_llm, 'invoke')}")
        
        # Test direct call
        response = gemini_llm.invoke("Hello")
        print(f"Direct invoke works: {response.content[:50]}...")
        
    except Exception as e:
        print(f"❌ LLM Wrapper Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing CrewAI compatibility with different LLMs...\n")
    
    # Test standalone Gemini first
    gemini_standalone = test_gemini_standalone()
    
    # Check LLM wrapper
    check_crewai_llm_wrapper()
    
    # Test CrewAI with different LLMs
    openai_works = test_crewai_with_default()
    gemini_works = test_crewai_with_gemini()
    
    print(f"\n=== Summary ===")
    print(f"Gemini Standalone: {'✅' if gemini_standalone else '❌'}")
    print(f"CrewAI + OpenAI: {'✅' if openai_works else '❌'}")
    print(f"CrewAI + Gemini: {'✅' if gemini_works else '❌'}")
    
    if gemini_standalone and not gemini_works:
        print("\n🔍 Conclusion: Gemini works fine standalone, but has issues with CrewAI integration")
        print("This suggests a compatibility issue between CrewAI and langchain-google-genai")