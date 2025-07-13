# Setup Guide for SF Itinerary Planner

This guide will help you set up the itinerary planner with real calendar integration from Google Calendar and Outlook.

## Prerequisites

- Python 3.8 or higher
- Google Calendar account (for Google Calendar integration)
- Microsoft 365 account (for Outlook integration)
- Event API keys (optional, for real event data)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Google Calendar Setup

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

### 2. Create Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download the credentials file
5. Rename it to `credentials.json` and place it in the project root

## Step 3: Outlook Calendar Setup

### 1. Register an Azure Application
1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" > "App registrations"
3. Click "New registration"
4. Fill in the details:
   - Name: "SF Itinerary Planner"
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: "Web" > "http://localhost:8000/callback"
5. Note down the Application (client) ID

### 2. Create a Client Secret
1. In your app registration, go to "Certificates & secrets"
2. Click "New client secret"
3. Add a description and choose expiration
4. Copy the secret value immediately (you won't see it again)

### 3. Set API Permissions
1. Go to "API permissions"
2. Click "Add a permission"
3. Choose "Microsoft Graph" > "Delegated permissions"
4. Add these permissions:
   - `Calendars.Read`
   - `Calendars.Read.Shared`

## Step 4: Environment Variables

Create a `.env` file in the project root with your credentials:

```env
# Google Calendar API Credentials
# (credentials.json file should be in project root)

# Outlook/Microsoft Graph API Credentials
OUTLOOK_CLIENT_ID=your_outlook_client_id_here
OUTLOOK_CLIENT_SECRET=your_outlook_client_secret_here
OUTLOOK_TENANT_ID=your_outlook_tenant_id_here

# Optional: Event API Keys
EVENTBRITE_API_KEY=your_eventbrite_api_key_here
TICKETMASTER_API_KEY=your_ticketmaster_api_key_here
```

## Step 5: Test Calendar Integration

Run the calendar integration test:

```bash
python src/planner/calendar_integration.py
```

This will:
- Test Google Calendar connection
- Test Outlook Calendar connection
- Show your calendar events for today

## Step 6: Run the Itinerary Planner

### Option 1: With Real Calendar Data
```bash
python src/planner/itinerary_with_calendar.py
```

### Option 2: With Mock Calendar Data
```bash
python src/planner/itinerary.py
```

## Troubleshooting

### Google Calendar Issues
- Make sure `credentials.json` is in the project root
- Check that Google Calendar API is enabled
- Verify your Google account has calendar events

### Outlook Calendar Issues
- Verify your Azure app registration is correct
- Check that the client secret hasn't expired
- Ensure you have the correct permissions

### API Key Issues
- Eventbrite and Ticketmaster API keys are optional
- The app will use mock data if API keys are not provided
- Get free API keys from:
  - [Eventbrite Developer Portal](https://www.eventbrite.com/platform/api-keys)
  - [Ticketmaster Developer Portal](https://developer-acct.ticketmaster.com/)

## Output

The planner will generate:
1. Console output showing the itinerary
2. A markdown file with the complete itinerary
3. Information about your calendar events and suggested activities

## Customization

You can customize:
- Location (change `self.location` in the code)
- Date (change `self.date` in the code)
- Event sources (modify `self.event_sources` list)
- Time range (modify day_start and day_end in `get_free_time_slots`)

## Security Notes

- Never commit your `.env` file or `credentials.json` to version control
- Keep your API keys secure
- The app only reads calendar data, it doesn't modify anything 