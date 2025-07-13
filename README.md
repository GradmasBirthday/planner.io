# SF Itinerary Planner

A smart itinerary planner that creates personalized day plans for San Francisco based on your calendar and local events.

## Features

- **Google Calendar Integration**: Connects to your Google Calendar to analyze your schedule
- **Smart Time Analysis**: Finds free time slots in your day
- **Calendar Summary**: Generates detailed summaries of your calendar events

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Google Calendar Integration
Create a `.env` file in the project root:
```env
# Google Calendar API Credentials
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### 3. Get Google Calendar Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Copy the Client ID and Client Secret
5. Add them to your `.env` file

### 4. Run the Calendar Analyzer
```bash
python src/planner/getschedule.py
```

## How It Works

1. **Google Calendar Connection**: Connects to your Google Calendar using OAuth
2. **Event Analysis**: Analyzes your calendar events for the current day
3. **Free Time Detection**: Identifies available time slots (8 AM - 10 PM)
4. **Summary Generation**: Creates a detailed summary of your day

## Output

The analyzer generates:
- Console output with your calendar summary
- `google_calendar_summary.md` file with the complete analysis

## Customization

You can easily customize:
- **Location**: Change `self.location` in the code
- **Date**: Modify `self.date` in the code
- **Time Range**: Adjust day_start and day_end in `get_free_time_slots`

## Project Structure

```
src/planner/
├── main.py              # Original crewAI entry point
├── getschedule.py       # 🎯 Google Calendar analyzer
├── crew.py              # CrewAI integration (legacy)
└── config/              # Configuration files
```

## Running Different Components

### Google Calendar Analyzer (Recommended)
```bash
python src/planner/getschedule.py
```

### Original CrewAI (requires crewai module)
```bash
python src/planner/main.py
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your Google API credentials secure
- The app only reads calendar data, it doesn't modify anything

## Support

For detailed setup instructions, see `SETUP_GUIDE.md`.
