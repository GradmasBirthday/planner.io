#!/usr/bin/env python3
"""
Simple test script to verify Gemini integration works
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini():
    """Test basic Gemini functionality"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        print("Please set your Google API key:")
        print("export GOOGLE_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Test simple query
        response = llm.invoke("Say 'Hello from Gemini!' and nothing else")
        print(f"✅ Gemini test successful!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Gemini integration...")
    test_gemini()