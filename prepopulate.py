import secrets
from app import app, db
from models import User, Events, APIKey

def preload_users():
    with app.app_context():
        if User.query.count() == 0:
            users = [
                ("Alice Johnson", "password1", True),
                ("Bob Smith", "password2", False),
                ("Charlie Davis", "password3", False),
                ("Diana Prince", "password4", True),
                ("Edward Norton", "password5", False),
                ("Fiona Gallagher", "password6", False),
                ("George Miller", "password7", True),
                ("Hannah Abbott", "password8", False),
                ("Ian Wright", "password9", False),
                ("Jenny Slate", "password10", False)
            ]
            for name, password, staff in users:
                user = User(fullname = name, staff = staff)
                user.set_password(password)
                db.session.add(user)
            #db.session.bulk_save_objects(users)
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