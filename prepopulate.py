import secrets
from app import app, db
from models import User, Events, APIKey

def preload_users():
    with app.app_context():
        if User.query.count() == 0:
            users = [
                User(fullname="Alice Johnson", password="password1", staff=True),
                User(fullname="Bob Smith", password="password2", staff=False),
                User(fullname="Charlie Davis", password="password3", staff=False),
                User(fullname="Diana Prince", password="password4", staff=True),
                User(fullname="Edward Norton", password="password5", staff=False),
                User(fullname="Fiona Gallagher", password="password6", staff=False),
                User(fullname="George Miller", password="password7", staff=True),
                User(fullname="Hannah Abbott", password="password8", staff=False),
                User(fullname="Ian Wright", password="password9", staff=False),
                User(fullname="Jenny Slate", password="password10", staff=False)
            ]
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("Preloaded users database")
        else:
            print("Users database already contains data")

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