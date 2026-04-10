from app import app, db
from models import User, Events

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        preload_users()