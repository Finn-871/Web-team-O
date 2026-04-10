import uuid
from utils import load_events, save_events

def get_all_events():
    return load_events()

def get_event(id):
    events = load_events()
    return next((e for e in events if e['id'] == id), None)

def create_event(data):
    events = load_events()

    new_event = {
        "id": str(uuid.uuid4()),
        "title": data.get("title"),
        "description": data.get("description"),
        "date": data.get("date"),
        "location": data.get("location")
    }

    events.append(new_event)
    save_events(events)

    return new_event

def update_event(id, data):
    events = load_events()

    for event in events:
        if event['id'] == id:
            event['title'] = data.get('title', event['title'])
            event['description'] = data.get('description', event['description'])
            event['date'] = data.get('date', event['date'])
            event['location'] = data.get('location', event['location'])

            save_events(events)
            return event

    return None

def delete_event(id):
    events = load_events()
    new_events = [e for e in events if e['id'] != id]

    if len(events) == len(new_events):
        return False

    save_events(new_events)
    return True
