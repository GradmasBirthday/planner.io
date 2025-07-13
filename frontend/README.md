# TripMaxx Frontend

AI-powered travel planning interface with Google Gemini integration.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env.local` file in the frontend directory with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_public_token_here
   ```

3. **Get your API Keys:**
   - **Google API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Mapbox Token**: Visit [Mapbox](https://account.mapbox.com/access-tokens/) to get your public token
   - Add both to your `.env.local` file

4. **Run the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000/chat](http://localhost:3000/chat)

## Features

- **Real-time AI Chat**: Powered by Google Gemini for intelligent travel planning
- **Interactive UI**: Modern chat interface with message history
- **Map Integration**: Mapbox-powered map view with location markers
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Beautiful icons
- **Mapbox GL**: Interactive maps

## API Integration

The chat interface connects to the backend Python script (`src/planner/api_handler.py`) which uses Google Gemini for travel planning. The backend:

1. Extracts travel parameters from user messages
2. Generates detailed travel planning prompts
3. Uses Gemini to create personalized itineraries
4. Returns structured responses to the frontend

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Troubleshooting

- **API Key Issues**: Make sure your `GOOGLE_API_KEY` is set correctly
- **Backend Connection**: Ensure the Python backend is accessible
- **Map Display**: Add your `NEXT_PUBLIC_MAPBOX_TOKEN` to view the map
