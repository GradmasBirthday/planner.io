# GetSchedule.py Setup Guide

This guide will help you set up the `getschedule.py` script to work with Google Calendar and Gmail integration.

## Prerequisites

- Python 3.8 or higher
- Google Calendar account
- Gmail account
- Gemini AI API key (for email analysis)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Google API Setup

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the required APIs:
   - Google Calendar API
   - Gmail API

### 2. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download the credentials file
5. Rename it to `credentials.json` and place it in the project root

## Step 3: Environment Variables

Create a `.env` file in the project root with:

```env
# Required: Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Mock responses for testing
MOCK_GEMINI=false
```

## Step 4: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## Step 5: Test the Script

```bash
cd src/planner
python getschedule.py
```

## Expected Output

The script will:
1. Connect to Google Calendar and Gmail
2. Generate a calendar summary for today
3. Search Gmail for travel/event emails
4. Extract structured event data using Gemini AI
5. Save results to `google_calendar_summary.md` and `extracted_events.json`

## Troubleshooting

### Google API Issues
- Make sure `credentials.json` is in the project root
- Check that Google Calendar and Gmail APIs are enabled
- Delete `token.pickle` and re-authenticate if needed

### Gemini API Issues
- Verify your `GEMINI_API_KEY` is set correctly
- Check API quota limits
- Use `MOCK_GEMINI=true` for testing without API calls

### File Structure
```
Planner/
├── credentials.json          ← Google API credentials
├── .env                      ← Environment variables
├── requirements.txt          ← Python dependencies
└── src/
    └── planner/
        ├── getschedule.py    ← Main script
        ├── tools/            ← Custom tools
        └── __init__.py       ← Package init
```

## Security Notes

- Never commit `credentials.json` or `.env` to version control
- Keep your API keys secure
- The app only reads calendar and email data 