# TripMaxxing - Personalized Itinerary Tailoring Assistant

Welcome to TripMaxxing, your personalized itinerary tailoring assistant that combines the power of AI agents with an intuitive user interface to create personalized travel experiences.

## 🚀 Features Implemented

### Core Frontend Features
- **Homepage**: Beautiful landing page showcasing TripMaxxing's features
- **AI Chat Interface**: Natural language trip planning with conversational AI
- **Travel Quiz**: Interactive preference assessment to create personalized travel personas
- **Itinerary Management**: Comprehensive trip planning and tracking interface
- **Responsive Design**: Mobile-first UI using Tailwind CSS

### AI Backend (CrewAI)
- **Trip Planner Agent**: Creates detailed itineraries based on preferences
- **Booking Agent**: Researches flights, hotels, and activities
- **Local Expert Agent**: Provides cultural insights and hidden gems
- **Custom Travel Tools**: Specialized tools for destination research, flight search, hotel search, and activity recommendations

## 🛠️ Technology Stack

### Frontend
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **React Hook Form** with Zod validation

### Backend
- **CrewAI** for multi-agent AI workflows
- **Python 3.12** 
- **Custom travel-focused tools and agents**

## 🏗️ Project Structure

```
TripMaxxing/
├── frontend/                 # Next.js frontend application
│   ├── src/app/             # App router pages
│   │   ├── chat/            # AI chat interface
│   │   ├── quiz/            # Travel preference quiz
│   │   ├── my-trips/        # Itinerary management
│   │   └── inspiration/     # Travel inspiration gallery
│   └── package.json
├── src/planner/             # CrewAI backend
│   ├── config/              # Agent and task configurations
│   ├── tools/               # Custom travel tools
│   └── crew.py              # Main crew orchestration
└── pyproject.toml
```

## 🚀 Getting Started

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```
Visit [http://localhost:3000](http://localhost:3000)

### Backend Development
```bash
# Install dependencies
pip install -e .

# Set up environment variables (now using Gemini instead of OpenAI)
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

# Test Gemini integration
python test_gemini.py

# Run the travel planning crew
crewai run
```

## 🎯 Key Features Showcase

### 1. Conversational AI Trip Planning
- Natural language processing for trip requests
- Real-time chat interface with AI travel assistant
- Contextual understanding of travel preferences

### 2. Personalized Travel Quiz
- 5-question assessment covering travel style, accommodation, activities, budget, and trip length
- AI-powered persona generation (Budget Adventurer, Cultural Connoisseur, etc.)
- Personalized recommendations based on quiz results

### 3. Comprehensive Itinerary Management
- Visual trip cards with progress tracking
- Detailed day-by-day activity planning
- Activity categorization (food, transport, accommodation, activities)
- Budget tracking and cost estimation

### 4. AI Agent Architecture
- **Trip Planner**: Creates structured itineraries with timing and logistics
- **Booking Agent**: Finds deals and booking options
- **Local Expert**: Provides cultural insights and authentic experiences

## 🔮 Future Enhancements

The current implementation provides a solid foundation for:
- Real API integrations (Amadeus, Google Maps, booking platforms)
- User authentication and profile management
- Social features and itinerary sharing
- Mobile app development
- Group collaboration tools
- Real-time booking and payment processing

## 🤖 AI Capabilities (Powered by Google Gemini)

TripMaxxing leverages CrewAI with Google Gemini (gemini-2.5-flash) to orchestrate specialized travel agents that work together to:
- Understand natural language travel requests using advanced LLM capabilities
- Research destinations and create personalized recommendations
- Find optimal booking options across multiple platforms
- Provide local insights and cultural guidance
- Generate comprehensive, actionable travel plans

**Why Gemini?**
- Faster response times compared to GPT models
- Strong multilingual support for international travel
- Excellent reasoning capabilities for complex trip planning
- Cost-effective for production deployment

## 🎨 Design Philosophy

TripMaxxing prioritizes:
- **User Experience**: Intuitive, conversational interfaces
- **Personalization**: AI-driven customization based on preferences
- **Comprehensive Planning**: End-to-end travel assistance
- **Visual Clarity**: Clean, modern design with clear information hierarchy
- **Mobile Accessibility**: Responsive design for planning on-the-go

---

Built with ❤️ using Next.js, CrewAI, and modern web technologies.
