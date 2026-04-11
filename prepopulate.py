import secrets
from app import app, db
from models import User, Events, APIKey
from datetime import datetime

def preload_users():
    with app.app_context():
        if User.query.count() == 0:
            users = [
                ("Alice Johnson", "JohnsonA176", "password1", True),
                ("Bob Smith", "SmithB159", "password2", False),
                ("Charlie Davis", "DavisC111", "password3", False),
                ("Diana Prince", "PrinceD285", "password4", True),
                ("Edward Norton", "NortonE490", "password5", False),
                ("Fiona Gallagher", "GallagherF277", "password6", False),
                ("George Miller", "MillerG968", "password7", True),
                ("Hannah Abbott", "AbbottH048", "password8", False),
                ("Ian Wright", "WrightI761", "password9", False),
                ("Jenny Slate", "SlateJ224", "password10", False)
            ]
            for name, username, password, staff in users:
                user = User(fullname = name, username = username, staff = staff)
                user.set_password(password)
                db.session.add(user)
            #db.session.bulk_save_objects(users)
            db.session.commit()
            print("Preloaded users database")
        else:
            print("Users database already contains data")

def preload_events():
    with app.app_context():
        if Events.query.count() == 0:
            events = [
                ("Computing Lecture", "Description here", datetime(2026, 5, 5, 12, 00), datetime(2026, 5, 5, 14, 00), 'Europe/London', "Building A, Room 5")
            ]
            for title, description, starts_at, ends_at, timeZone, venue in events:
                event = Events(title = title, description = description, starts_at = starts_at, ends_at = ends_at, timezone = timeZone, venue = venue)
                db.session.add(event)
            db.session.commit()
            print("Preloaded events database")
        else:
            print("events database already contains data")

def preload_api_keys():
    with app.app_context():
        if APIKey.query.count() == 0:
            api_keys = [
                {"owner": "Frontend App"},
                {"owner": "Staff"},
                {"owner": "Student"},
            ]
            for entry in api_keys:
                new_key = APIKey(
                    key=secrets.token_hex(32),
                    owner=entry["owner"],
                    rate_limit=1000
                )
                db.session.add(new_key)
            db.session.commit()
            print("API keys successfully created")
        else:
            print("API keys already exist")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        preload_api_keys()
        preload_users()
        preload_events()