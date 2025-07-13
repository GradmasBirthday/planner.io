# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TripMaxx is an AI-powered travel companion that combines a Next.js frontend with a CrewAI-based backend for intelligent travel planning. The application features conversational AI trip planning, personalized travel quizzes, and comprehensive itinerary management with a modern red-themed interface.

## Architecture

### Frontend (Next.js App)
- **Location**: `/frontend/`
- **Framework**: Next.js 15 with App Router, TypeScript, Tailwind CSS
- **Branding**: TripMaxx with custom red-themed logo and styling
- **Key Pages**: 
  - `/` - Landing page with TripMaxx branding and feature showcase
  - `/chat` - Conversational AI trip planning interface with sidebar layout
  - `/quiz` - Interactive travel preference assessment
  - `/my-trips` - Itinerary management and trip tracking
  - `/inspiration` - Travel inspiration gallery
- **State Management**: React useState hooks for local state
- **Styling**: Tailwind CSS with Lucide React icons, red theme throughout
- **Components**: Modular architecture with reusable UI components

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
Backend uses Google Gemini and frontend requires Mapbox integration:
- Required: `GOOGLE_API_KEY` environment variable for AI functionality
- Required: `NEXT_PUBLIC_MAPBOX_TOKEN` for map functionality
- Optional: `OPENAI_API_KEY` for fallback (legacy support)

Create `.env.local` file in frontend directory:
```
GOOGLE_API_KEY=your_google_api_key_here
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_public_token_here
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

### TripMaxx UI Components
- **TripMaxxLogo**: Custom logo component with airplane and globe icons
- **AppSidebar**: Navigation sidebar with TripMaxx branding
- **ChatInterface**: Real-time chat with Gemini integration
- **MapView**: Automatic Mapbox integration with environment variables
- **UI Components**: Reusable Button and Input components with red theme

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
- Red theme throughout with no gradients for clean, modern appearance

### Travel Tools Implementation
Custom CrewAI tools extend `BaseTool` with Pydantic schemas:
- `DestinationResearchTool` - Comprehensive destination information
- `FlightSearchTool` - Flight options and pricing
- `HotelSearchTool` - Accommodation recommendations
- `ActivitySearchTool` - Local activities and experiences

Currently tools return simulated data; production implementation would integrate real travel APIs (Amadeus, Google Maps, booking platforms).

### Map Integration
- **Automatic Setup**: Mapbox token automatically loaded from `NEXT_PUBLIC_MAPBOX_TOKEN`
- **No User Input**: No manual token entry required
- **Error Handling**: Clear error messages when token not configured
- **Red Theme**: Map markers styled to match TripMaxx branding
- **Tokyo Locations**: Pre-configured locations for demonstration

### Data Flow
1. User interacts with frontend (chat, quiz, trip management)
2. Frontend calls backend agents via travel crew execution
3. Agents use specialized tools to research and plan
4. Results formatted as structured data (JSON/Markdown)
5. Frontend displays results in interactive interfaces

## File Structure Significance

- `/frontend/src/app/` - Next.js App Router pages with TypeScript
- `/frontend/src/components/` - Reusable UI components including TripMaxxLogo
- `/frontend/src/components/ui/` - Base UI components (Button, Input)
- `/frontend/src/lib/` - Utility functions and helpers
- `/src/planner/config/` - CrewAI agent and task YAML configurations
- `/src/planner/tools/` - Custom travel research and booking tools
- `/src/planner/crew.py` - Main orchestration class binding agents and tasks
- `/pyproject.toml` - Python package configuration with CrewAI scripts
- `/frontend/package.json` - Frontend dependencies and build scripts

## Recent Updates

### Branding Changes
- **TripMaxx**: Rebranded from "mindtrip" to "TripMaxx"
- **Red Theme**: Complete color scheme update from blue/purple gradients to solid red
- **Custom Logo**: Airplane and globe icon with "Travel AI" tagline
- **Consistent Styling**: Red theme applied throughout all components

### Technical Improvements
- **Automatic Mapbox**: Environment variable integration removes manual token entry
- **Enhanced Error Handling**: Clear error messages for missing API keys
- **Improved UX**: No more manual input prompts for map functionality
- **TypeScript**: Better type safety and component interfaces

The architecture separates AI logic (CrewAI agents) from user interface (Next.js), enabling independent development and deployment of backend intelligence and frontend experience with modern TripMaxx branding.