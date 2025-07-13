#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv("OPENAI_API_KEY"))

from planner.crew import Planner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew for travel planning.
    """
    inputs = {
        'destination': 'Tokyo, Japan',
        'duration': '5',
        'travel_style': 'foodie and cultural exploration',
        'budget': '$2000-3000',
        'interests': 'authentic cuisine, local markets, cultural sites, traditional experiences',
        'accommodation_type': 'boutique hotels or traditional ryokans'
    }
    
    try:
        result = Planner().crew().kickoff(inputs=inputs)
        print("Travel planning completed successfully!")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the travel crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'destination': 'Paris, France',
        'duration': '7',
        'travel_style': 'cultural and romantic',
        'budget': '$3000-4000',
        'interests': 'art, history, cuisine, architecture',
        'accommodation_type': 'boutique hotels'
    }
    try:
        Planner().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Planner().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'destination': 'Bali, Indonesia',
        'duration': '10',
        'travel_style': 'wellness and adventure',
        'budget': '$1500-2500',
        'interests': 'yoga, nature, local culture, beaches',
        'accommodation_type': 'eco-resorts and wellness retreats'
    }
    
    try:
        Planner().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
