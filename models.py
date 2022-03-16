# from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, password, phone, email, address, pincode):
        self.name = name
        self.password = generate_password_hash(password)
        self.phone = phone
        self.email = email
        self.address = address
        self.pincode = pincode

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return '<User %r>' % self.name