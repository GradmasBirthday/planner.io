# Gemini API Proxy Server Setup

This setup creates a Python FastAPI server that acts as a proxy for the Gemini API, allowing your Next.js frontend to communicate with Gemini through a simple HTTP API.

## Files Created

1. **`src/planner/gemini_server.py`** - FastAPI server with Gemini integration
2. **`requirements.txt`** - Python dependencies
3. **`start_gemini_server.py`** - Startup script with environment checks
4. **`frontend/src/app/api/chat/route.ts`** - Updated to call Python server

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

### 3. Start the Python Server

```bash
python start_gemini_server.py
```

Or directly with uvicorn:
```bash
uvicorn src.planner.gemini_server:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start the Next.js Frontend

```bash
cd frontend
npm run dev
```

## API Endpoints

- **GET `/`** - Server status
- **POST `/chat`** - Chat with Gemini
- **GET `/health`** - Health check
- **GET `/docs`** - API documentation (Swagger UI)

## Usage

The frontend will now call the Python server at `http://localhost:8000/chat` instead of calling Gemini directly. The Python server handles all Gemini API communication.

## Troubleshooting

1. **Missing GOOGLE_API_KEY**: Make sure your `.env` file has the correct API key
2. **Port 8000 in use**: Change the PORT in `.env` or kill the process using port 8000
3. **CORS issues**: The server allows all origins for development. Adjust for production.

## Architecture

```
Frontend (Next.js) → Python FastAPI Server → Gemini API
```

The Python server acts as a middleware, handling all Gemini API calls and providing a simple HTTP interface for the frontend. 