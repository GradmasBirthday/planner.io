import os
import pickle
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ItineraryItem:
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    city: str

class ItineraryManager:
    def __init__(self):
        self.calendar_service = None
        self.gmail_service = None
        self.setup_google_services()

    def setup_google_services(self):
        """Setup Google Calendar and Gmail API services"""
        try:
            SCOPES = [
                'https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/gmail.send'
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

            self.calendar_service = build('calendar', 'v3', credentials=creds)
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            print("✅ Google Calendar and Gmail connected successfully")

        except Exception as e:
            print(f"❌ Google API setup failed: {e}")
            self.calendar_service = None
            self.gmail_service = None

    def load_itinerary(self, file_path: str = "itinerary.json") -> List[ItineraryItem]:
        """Load itinerary items from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            items = []
            for item in data:
                # Parse ISO 8601 datetime strings
                start_time = datetime.fromisoformat(item['start_time'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(item['end_time'].replace('Z', '+00:00'))
                
                # Convert to America/Los_Angeles timezone
                local_tz = pytz.timezone('America/Los_Angeles')
                start_time = start_time.astimezone(local_tz)
                end_time = end_time.astimezone(local_tz)
                
                items.append(ItineraryItem(
                    title=item['title'],
                    description=item['description'],
                    start_time=start_time,
                    end_time=end_time,
                    location=item['location'],
                    city=item['city']
                ))
            
            print(f"📋 Loaded {len(items)} itinerary items from {file_path}")
            return items
            
        except FileNotFoundError:
            print(f"❌ Itinerary file not found: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error loading itinerary: {e}")
            return []

    def add_calendar_event(self, item: ItineraryItem) -> bool:
        """Add a single itinerary item to Google Calendar"""
        if not self.calendar_service:
            print("❌ Calendar service not available")
            return False
        
        try:
            event = {
                'summary': item.title,
                'description': item.description,
                'location': item.location,
                'start': {
                    'dateTime': item.start_time.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': item.end_time.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
            }

            event = self.calendar_service.events().insert(
                calendarId='primary',
                body=event
            ).execute()

            print(f"✅ Added calendar event: {item.title} at {item.start_time.strftime('%I:%M %p')}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding calendar event '{item.title}': {e}")
            return False

    def sync_itinerary_to_calendar(self, items: List[ItineraryItem]) -> int:
        """Sync all itinerary items to Google Calendar"""
        if not items:
            print("📝 No itinerary items to sync")
            return 0
        
        success_count = 0
        for item in items:
            if self.add_calendar_event(item):
                success_count += 1
        
        print(f"📅 Successfully synced {success_count}/{len(items)} events to Google Calendar")
        return success_count

    def create_email_content(self, items: List[ItineraryItem]) -> str:
        """Create formatted HTML email content"""
        if not items:
            return "<p>No itinerary items found.</p>"
        
        # Group items by city
        city_groups = {}
        for item in items:
            city = item.city
            if city not in city_groups:
                city_groups[city] = []
            city_groups[city].append(item)
        
        # Get the first date for the subject
        first_date = items[0].start_time.strftime('%B %d, %Y')
        first_city = items[0].city
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .city-section {{ margin-bottom: 30px; }}
                .city-title {{ color: #2c3e50; font-size: 18px; font-weight: bold; margin-bottom: 15px; }}
                .event-item {{ margin-bottom: 10px; padding-left: 20px; }}
                .event-time {{ color: #7f8c8d; font-weight: bold; }}
                .event-title {{ color: #2c3e50; font-weight: bold; }}
                .event-location {{ color: #95a5a6; font-style: italic; }}
                .event-description {{ color: #34495e; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🗓️ Your Trip Itinerary</h1>
                <p><strong>Date:</strong> {first_date}</p>
                <p><strong>Destination:</strong> {first_city}</p>
            </div>
        """
        
        for city, city_items in city_groups.items():
            html_content += f'<div class="city-section">\n'
            html_content += f'<div class="city-title">📍 {city}</div>\n'
            
            # Sort items by start time
            sorted_items = sorted(city_items, key=lambda x: x.start_time)
            
            for item in sorted_items:
                time_str = item.start_time.strftime('%I:%M %p')
                end_time_str = item.end_time.strftime('%I:%M %p')
                
                html_content += f'''
                <div class="event-item">
                    <div class="event-time">🕐 {time_str} - {end_time_str}</div>
                    <div class="event-title">• {item.title}</div>
                    <div class="event-location">📍 {item.location}</div>
                    <div class="event-description">{item.description}</div>
                </div>
                '''
            
            html_content += '</div>\n'
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content

    def send_itinerary_email(self, items: List[ItineraryItem], recipient: str = "shaunlewis226@gmail.com") -> bool:
        """Send formatted itinerary email via Gmail API"""
        if not self.gmail_service:
            print("❌ Gmail service not available")
            return False
        
        if not items:
            print("📝 No itinerary items to send")
            return False
        
        try:
            # Create email content
            html_content = self.create_email_content(items)
            
            # Create email message
            message = MIMEMultipart('alternative')
            message['to'] = recipient
            message['subject'] = "Your Trip Itinerary ✈️"
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Encode the message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send the email
            self.gmail_service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"📧 Successfully sent itinerary email to {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False

def main():
    """Main function to sync itinerary and send email"""
    print("🚀 Starting Itinerary Sync and Email Process")
    print("=" * 50)
    
    # Initialize manager
    manager = ItineraryManager()
    
    # Load itinerary
    items = manager.load_itinerary()
    if not items:
        print("❌ No itinerary items loaded. Exiting.")
        return
    
    # Sync to calendar
    print("\n📅 Syncing to Google Calendar...")
    synced_count = manager.sync_itinerary_to_calendar(items)
    
    # Send email
    print("\n📧 Sending itinerary email...")
    email_sent = manager.send_itinerary_email(items)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"   • Total itinerary items: {len(items)}")
    print(f"   • Calendar events added: {synced_count}")
    print(f"   • Email sent: {'✅ Yes' if email_sent else '❌ No'}")
    print("=" * 50)

if __name__ == "__main__":
    main() 