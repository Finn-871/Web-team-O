from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique id for users
    fullname = db.Column(db.String(120), nullable=False) #users name
    password = db.Column(db.String(120), nullable=False) #users password
    staff = db.Column(db.Boolean, default=False, nullable=False) #boolean to differentiate staff from students

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True) #unique id for events
