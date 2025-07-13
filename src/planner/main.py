#!/usr/bin/env python
"""
Main entry point for the Planner Crew.
"""

from crew import PlannerCrew

def main():
    """
    Main function to run the Planner Crew.
    """
    # Create the crew
    crew = PlannerCrew()
    
    # Run the crew
    result = crew.run()
    
    # Print the result
    print("\n" + "="*50)
    print("CREW RESULT")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
