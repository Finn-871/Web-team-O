import json
import os
from googleapiclient.discovery import build

DATA_FILE = 'events.json'

def load_events():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_events(events):
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=2)


def add_event_to_google(event_data, creds):
    service = build('calendar', 'v3', credentials=creds)
    g_event = {
        'summary': event_data.title,
        'location': event_data.venue,
        'description': event_data.description,
        'start': {
            'dateTime': event_data.starts_at.isoformat(),
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': event_data.ends_at.isoformat(),
            'timeZone': 'Europe/London',
        },
    }
    return service.events().insert(calendarId='primary', body=g_event).execute()