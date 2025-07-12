# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Voyagia is an AI-powered travel companion that combines a Next.js frontend with a CrewAI-based backend for intelligent travel planning. The application features conversational AI trip planning, personalized travel quizzes, and comprehensive itinerary management.

## Architecture

### Frontend (Next.js App)
- **Location**: `/frontend/`
- **Framework**: Next.js 15 with App Router, TypeScript, Tailwind CSS
- **Key Pages**: 
  - `/` - Landing page with feature showcase
  - `/chat` - Conversational AI trip planning interface
  - `/quiz` - Interactive travel preference assessment
  - `/my-trips` - Itinerary management and trip tracking
  - `/inspiration` - Travel inspiration gallery
- **State Management**: React useState hooks for local state
- **Styling**: Tailwind CSS with Lucide React icons

### Backend (CrewAI Agents)
- **Location**: `/src/planner/`
- **Framework**: CrewAI multi-agent system
- **Agent Architecture**: Three specialized agents working sequentially:
  - `trip_planner` - Creates detailed itineraries based on preferences
  - `booking_agent` - Researches flights, hotels, and activities
  - `local_expert` - Provides cultural insights and hidden gems
- **Tools**: Custom travel tools in `/src/planner/tools/travel_tools.py`
- **Configuration**: Agent and task definitions in `/src/planner/config/`

## Development Commands

### Frontend Development
```bash
cd frontend
npm install           # Install dependencies
npm run dev          # Start development server (localhost:3000)
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Backend Development
```bash
pip install -e .     # Install package in development mode
crewai run           # Run the travel planning crew
crewai train <n> <file>  # Train the crew for n iterations
crewai replay <task_id>  # Replay specific task execution
crewai test <n> <llm>    # Test crew with evaluation
```

### Environment Setup
Backend now uses Google Gemini instead of OpenAI:
- Required: `GOOGLE_API_KEY` environment variable for AI functionality
- Optional: `OPENAI_API_KEY` for fallback (legacy support)

Create `.env` file in project root:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Key Implementation Details

### Direct Gemini Integration (Production)
The current implementation uses Google Gemini (gemini-2.5-flash) directly for travel planning, bypassing CrewAI due to compatibility issues. This approach provides:
- Faster response times
- More reliable execution
- Simplified debugging and maintenance

The system works as follows:
1. Extracts travel parameters from natural language input
2. Generates comprehensive travel planning prompts
3. Uses Gemini to create detailed day-by-day itineraries
4. Returns structured travel plans with recommendations

### Frontend-Backend Integration
- Frontend chat calls `/api/chat` Next.js API route
- API route spawns Python process running `src/planner/api_handler.py`
- Handler uses `langchain-google-genai` to call Gemini directly
- Results flow back through JSON response to chat interface
- Falls back to demo mode if `GOOGLE_API_KEY` not configured

### CrewAI Multi-Agent System (Development)
The CrewAI configuration exists for future development when compatibility issues are resolved:
- `src/planner/config/agents.yaml` - Agent definitions for trip planning, booking, and local expertise
- `src/planner/config/tasks.yaml` - Task configurations for sequential agent execution
- `src/planner/crew.py` - Crew orchestration (currently not used in production due to LLM integration issues)

### Frontend Component Architecture
- Pages use client-side state with `'use client'` directive
- Shared UI patterns: modals, cards, progress indicators
- TypeScript interfaces define data structures for trips, itineraries, and quiz responses
- Responsive design with mobile-first approach

### Travel Tools Implementation
Custom CrewAI tools extend `BaseTool` with Pydantic schemas:
- `DestinationResearchTool` - Comprehensive destination information
- `FlightSearchTool` - Flight options and pricing
- `HotelSearchTool` - Accommodation recommendations
- `ActivitySearchTool` - Local activities and experiences

Currently tools return simulated data; production implementation would integrate real travel APIs (Amadeus, Google Maps, booking platforms).

### Data Flow
1. User interacts with frontend (chat, quiz, trip management)
2. Frontend calls backend agents via travel crew execution
3. Agents use specialized tools to research and plan
4. Results formatted as structured data (JSON/Markdown)
5. Frontend displays results in interactive interfaces

## File Structure Significance

- `/frontend/src/app/` - Next.js App Router pages with TypeScript
- `/src/planner/config/` - CrewAI agent and task YAML configurations
- `/src/planner/tools/` - Custom travel research and booking tools
- `/src/planner/crew.py` - Main orchestration class binding agents and tasks
- `/pyproject.toml` - Python package configuration with CrewAI scripts
- `/frontend/package.json` - Frontend dependencies and build scripts

The architecture separates AI logic (CrewAI agents) from user interface (Next.js), enabling independent development and deployment of backend intelligence and frontend experience.