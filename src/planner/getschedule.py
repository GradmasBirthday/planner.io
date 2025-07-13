import os
import pickle
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import pytz
from dateutil import parser as dateparser
import google.generativeai as genai
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import re
load_dotenv()

@dataclass(frozen=True)
class TimeSlot:
    start_time: datetime
    end_time: datetime
    is_busy: bool

@dataclass
class CalendarEvent:
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    source: str
    event_id: str
    is_all_day: bool = False

class GoogleCalendarManager:
    def __init__(self):
        self.location = "San Francisco, CA"
        self.date = datetime.now().date()
        self.google_service = None
        self.gmail_service = None
        self.setup_google_services()

    def setup_google_services(self):
        print("If Gmail isn't working, delete token.pickle and re-run to re-authenticate with Gmail scopes.")
        try:
            SCOPES = [
                'https://www.googleapis.com/auth/calendar.readonly',
                'https://www.googleapis.com/auth/gmail.readonly'
            ]
            creds = None

            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid or not set(SCOPES).issubset(set(getattr(creds, 'scopes', []))):
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=8080)
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            self.google_service = build('calendar', 'v3', credentials=creds)
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            print("✅ Google Calendar and Gmail connected successfully")

        except Exception as e:
            print(f"❌ Google API setup failed: {e}")
            self.google_service = None
            self.gmail_service = None

    def get_google_calendar_events(self, start_date: datetime, end_date: datetime) -> List[CalendarEvent]:
        if not self.google_service:
            return []
        try:
            local_tz = pytz.timezone('America/Los_Angeles')
            start_local = local_tz.localize(datetime.combine(start_date.date(), datetime.min.time()))
            end_local = local_tz.localize(datetime.combine(end_date.date(), datetime.min.time()))

            events_result = self.google_service.events().list(
                calendarId='primary',
                timeMin=start_local.isoformat(),
                timeMax=end_local.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            calendar_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                if 'T' in start:
                    start_time = datetime.fromisoformat(start.replace('Z', '+00:00')) if 'Z' in start else datetime.fromisoformat(start)
                    end_time = datetime.fromisoformat(end.replace('Z', '+00:00')) if 'Z' in end else datetime.fromisoformat(end)
                    is_all_day = False
                else:
                    start_time = datetime.fromisoformat(start)
                    end_time = datetime.fromisoformat(end)
                    is_all_day = True

                calendar_events.append(CalendarEvent(
                    title=event.get('summary', 'No Title'),
                    description=event.get('description'),
                    start_time=start_time,
                    end_time=end_time,
                    location=event.get('location'),
                    source='google',
                    event_id=event['id'],
                    is_all_day=is_all_day
                ))
            return calendar_events
        except Exception as e:
            print(f"❌ Error fetching calendar events: {e}")
            return []

    def get_all_calendar_events(self, date: datetime) -> List[CalendarEvent]:
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return self.get_google_calendar_events(start_date, end_date)

    def get_free_time_slots(self) -> List[TimeSlot]:
        local_tz = pytz.timezone('America/Los_Angeles')
        day_start = local_tz.localize(datetime.combine(self.date, datetime.min.time().replace(hour=8)))
        day_end = local_tz.localize(datetime.combine(self.date, datetime.min.time().replace(hour=22)))

        calendar_events = self.get_all_calendar_events(datetime.combine(self.date, datetime.min.time()))
        busy_slots = [
            TimeSlot(event.start_time, event.end_time, True)
            for event in calendar_events if not event.is_all_day
        ]

        free_slots = []
        current_time = day_start
        for busy in sorted(busy_slots, key=lambda x: x.start_time):
            if current_time < busy.start_time:
                free_slots.append(TimeSlot(current_time, busy.start_time, False))
            current_time = max(current_time, busy.end_time)
        if current_time < day_end:
            free_slots.append(TimeSlot(current_time, day_end, False))

        return free_slots

    def generate_calendar_summary(self) -> str:
        calendar_events = self.get_all_calendar_events(datetime.combine(self.date, datetime.min.time()))
        free_slots = self.get_free_time_slots()

        summary = f"""
# Your Google Calendar Summary for {self.date.strftime('%A, %B %d, %Y')}

## 📍 Location: {self.location}

## 📅 Your Calendar Events:
"""
        if calendar_events:
            for event in calendar_events:
                time_str = event.start_time.strftime("%I:%M %p")
                end_str = event.end_time.strftime("%I:%M %p")
                location_info = f" at {event.location}" if event.location else ""
                all_day = " (All Day)" if event.is_all_day else ""
                summary += f"- {time_str} - {end_str}: {event.title}{location_info}{all_day} ({event.source})\n"
        else:
            summary += "- No events found for this day\n"

        summary += "\n## 🕐 Your Free Time Slots:\n"
        if free_slots:
            for i, slot in enumerate(free_slots, 1):
                summary += f"{i}. {slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}\n"
        else:
            summary += "- No free time slots found\n"

        summary += f"""
## 📊 Summary:
- Total Events: {len(calendar_events)}
- Free Time Slots: {len(free_slots)}
- Date: {self.date.strftime('%A, %B %d, %Y')}
- Calendar: Google Calendar
"""
        return summary

    def search_gmail_emails(self, query: str, max_results: int = 10) -> list:
        if not self.gmail_service:
            print("Gmail service not initialized.")
            return []
        try:
            results = self.gmail_service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            messages = results.get('messages', [])
            emails = []
            for msg in messages:
                msg_detail = self.gmail_service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From']
                ).execute()
                headers = {h['name']: h['value'] for h in msg_detail.get('payload', {}).get('headers', [])}
                subject = headers.get('Subject', '(No Subject)')
                sender = headers.get('From', '(No Sender)')
                snippet = msg_detail.get('snippet', '')
                emails.append({
                    'subject': subject,
                    'sender': sender,
                    'snippet': snippet
                })
            return emails
        except Exception as e:
            print(f"❌ Error searching Gmail: {e}")
            return []

def is_email_relevant(snippet: str, subject: str, keywords: list) -> bool:
    score = 0
    content = f"{subject} {snippet}".lower()
    for word in keywords:
        if word.lower() in content:
            score += 1
    return score >= 2

def call_gemini_for_event(prompt: str) -> Optional[dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables")
    
    # Mock responses for testing when API limit is hit
    mock_responses = {
        "Your Boarding Pass for United Flight 214": {
            "type": "airline",
            "subject": "Your Boarding Pass for United Flight 214",
            "start_date": "2025-07-19",
            "end_date": "2025-07-19",
            "city": "San Francisco"
        },
        "Booking Confirmed – NYC Grand Hotel": {
            "type": "hotel",
            "subject": "Booking Confirmed – NYC Grand Hotel",
            "start_date": "2025-07-15",
            "end_date": "2025-07-18",
            "city": "New York City"
        },
        "You're on the List – Drake Concert SF": {
            "type": "concert",
            "subject": "You're on the List – Drake Concert SF",
            "start_date": "2025-07-20",
            "end_date": "2025-07-20",
            "city": "San Francisco"
        },
        "Your order confirmation for \"Spotify Premium\"": None  # This should be filtered out
    }
    
    try:
        # Check if we should use mock responses (API limit hit)
        if "429" in str(os.getenv("MOCK_GEMINI", "")) or "quota" in str(os.getenv("MOCK_GEMINI", "")):
            # Extract subject from prompt to match mock response
            subject_match = re.search(r'Subject: ([^\n]+)', prompt)
            if subject_match:
                subject = subject_match.group(1).strip()
                return mock_responses.get(subject)
            return None
        
        # Real API call
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        try:
            output = response.candidates[0].content.parts[0].text
            output = re.sub(r"^```json\s*|^```|```$", "", output.strip(), flags=re.MULTILINE).strip()
            parsed = json.loads(output)
            
            # Return None if Gemini returned null or invalid data
            if parsed is None or parsed.get("type") == "unknown" or parsed.get("subject") == "unknown":
                return None
                
            # Validate that we have meaningful data
            if not parsed.get("type") or not parsed.get("subject"):
                return None
                
            return parsed
        except Exception as e:
            print(f"❌ Error parsing Gemini response: {e}")
            return None
    except Exception as e:
        print(f"❌ Error calling Gemini: {e}")
        return None

def main():
    calendar_manager = GoogleCalendarManager()
    summary = calendar_manager.generate_calendar_summary()
    with open("google_calendar_summary.md", "w", encoding="utf-8") as f:
        f.write(summary)

    keyword_queries = {
        "airline": {
            "query": "subject:(airline OR Flight OR boarding OR itinerary OR booking OR flight) newer_than:30d",
            "keywords": ["airline", "Flight", "boarding", "ticket", "itinerary", "flight"]
        },
        "hotels": {
            "query": "subject:(hotel OR reservation OR check-in OR booking) newer_than:30d",
            "keywords": ["hotel", "reservation", "check-in", "stay"]
        },
        "tickets": {
            "query": "subject:(ticket OR pass OR admission OR booking) newer_than:30d",
            "keywords": ["ticket", "entry", "qr code", "seat", "pass"]
        },
        "booking": {
            "query": "subject:(booking OR reservation OR confirmation) newer_than:30d",
            "keywords": ["booking", "confirmation", "reference", "id"]
        },
        "events": {
            "query": "subject:(event OR invitation OR RSVP OR guestlist OR Concert OR party OR concert) newer_than:30d",
            "keywords": ["event", "invitation", "rsvp", "Concert", "party", "concert"]
        }
    }

    structured_results = []
    for label, meta in keyword_queries.items():
        query = meta["query"]
        keywords = meta["keywords"]
        raw_emails = calendar_manager.search_gmail_emails(query)
        filtered_emails = [
            email for email in raw_emails
            if is_email_relevant(email['snippet'], email['subject'], keywords)
        ]
        # Print the raw emails for this label/keyword
        print(f"\n[Raw Gmail Results for '{label}']")
        print(json.dumps(filtered_emails, indent=2))
        for email in filtered_emails:
            prompt = f"""
You are an expert at extracting structured event information from emails. Analyze the following email and extract ONLY the relevant travel, hotel, or event details.

INSTRUCTIONS:
- Only extract information if this email contains actual travel, hotel, or event details
- If the email is not relevant (like a Spotify subscription), return null
- For dates, use YYYY-MM-DD format when possible, or the exact date mentioned
- For cities, extract the actual city name mentioned
- Be specific with the type: "airline", "hotel", "concert", "event", "restaurant", etc.

REQUIRED OUTPUT FORMAT:
Return a JSON object with these exact keys:
{{
  "type": "specific_type_here",
  "subject": "email_subject",
  "start_date": "YYYY-MM-DD or exact date mentioned",
  "end_date": "YYYY-MM-DD or exact date mentioned (use start_date if same)",
  "city": "city_name"
}}

If you cannot extract meaningful information, return null instead of making up data.

EMAIL TO ANALYZE:
Subject: {email.get("subject", "")}
Content: {email.get("snippet", "")}
"""
            event_info = call_gemini_for_event(prompt)
            if event_info is not None:
                structured_results.append(event_info)
    # Print all structured results once at the end
    print(json.dumps(structured_results, indent=2))
    with open("extracted_events.json", "w") as f:
        json.dump(structured_results, f, indent=2)

if __name__ == "__main__":
    main()
