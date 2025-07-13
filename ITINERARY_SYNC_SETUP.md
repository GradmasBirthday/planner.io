# Itinerary Sync and Email Setup Guide

This guide will help you set up the `itinerary_sync_and_email.py` script to sync itinerary items to Google Calendar and send formatted emails.

## Prerequisites

- Python 3.8 or higher
- Google Calendar account
- Gmail account
- Google Cloud Project with APIs enabled

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

## Step 3: Prepare Your Itinerary Data

### Option 1: Use the provided sample itinerary
The script comes with a sample `itinerary.json` file with San Francisco activities.

### Option 2: Create your own itinerary
Create an `itinerary.json` file in the `src/planner/` directory with this format:

```json
[
  {
    "title": "Activity Title",
    "description": "Detailed description of the activity",
    "start_time": "2025-07-25T10:00:00Z",
    "end_time": "2025-07-25T11:30:00Z",
    "location": "Specific location or address",
    "city": "City name"
  }
]
```

**Important Notes:**
- Use ISO 8601 format for dates (YYYY-MM-DDTHH:MM:SSZ)
- Times should be in UTC
- The script will automatically convert to America/Los_Angeles timezone

## Step 4: Configure Email Settings

### Default Email Recipient
The script is configured to send emails to `shaunlewis226@gmail.com` by default.

To change the recipient, modify line 217 in `itinerary_sync_and_email.py`:

```python
def send_itinerary_email(self, items: List[ItineraryItem], recipient: str = "your-email@gmail.com") -> bool:
```

## Step 5: Test the Script

```bash
cd src/planner
python itinerary_sync_and_email.py
```

## Expected Output

The script will:
1. Connect to Google Calendar and Gmail APIs
2. Load itinerary items from `itinerary.json`
3. Add each item as a calendar event
4. Send a formatted HTML email with the itinerary
5. Display a summary of actions taken

## Features

### Calendar Integration
- Automatically creates Google Calendar events
- Includes title, description, location, and time
- Uses America/Los_Angeles timezone
- Handles timezone conversion from UTC

### Email Functionality
- Sends beautifully formatted HTML emails
- Groups activities by city
- Includes styling for better readability
- Shows times, locations, and descriptions

### Error Handling
- Graceful handling of missing files
- API error reporting
- Authentication failure recovery

## Troubleshooting

### Google API Issues
- Make sure `credentials.json` is in the project root
- Check that Google Calendar and Gmail APIs are enabled
- Delete `token.pickle` and re-authenticate if needed
- Verify your Google account has calendar and Gmail access

### Itinerary File Issues
- Ensure `itinerary.json` is in the `src/planner/` directory
- Check JSON format is valid
- Verify date/time format is ISO 8601

### Email Issues
- Check that Gmail API is enabled
- Verify the recipient email address
- Ensure your Google account has Gmail access

## File Structure

```
Planner/
├── credentials.json                    ← Google API credentials
├── requirements.txt                    ← Python dependencies
└── src/
    └── planner/
        ├── itinerary_sync_and_email.py ← Main script
        ├── itinerary.json              ← Sample itinerary data
        └── __init__.py                 ← Package init
```

## Security Notes

- Never commit `credentials.json` to version control
- Keep your API keys secure
- The app creates calendar events and sends emails
- Only reads from `itinerary.json`, doesn't modify it

## Customization

You can customize:
- Email recipient (modify the default parameter)
- Timezone (change 'America/Los_Angeles' in the code)
- Email styling (modify the HTML/CSS in `create_email_content`)
- Calendar event format (modify the event structure in `add_calendar_event`) 