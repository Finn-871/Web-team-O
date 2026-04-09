from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    staff = db.Column(db.Boolean, default=False)

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, unique=True, primary_key=True)

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, unique=True, primary_key=True)