from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique id for users
    fullname = db.Column(db.String(120), nullable=False) #users name
    password = db.Column(db.String(256), nullable=False) #users password
    staff = db.Column(db.Boolean, default=False, nullable=False) #boolean to differentiate staff from students

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True) #unique id for events

class APIKey(db.Model):
    __bind_key__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    owner = db.Column(db.String(50), nullable=False)
    request_count = db.Column(db.Integer, default=0)
    rate_limit = db.Column(db.Integer, default=1000)
