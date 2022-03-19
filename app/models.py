# from app import db
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
db = SQLAlchemy()
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    is_restaurent = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, password, phone, email, address, pincode):
        self.name = name
        self.password = generate_password_hash(password,method='pbkdf2:sha256', salt_length=8)
        self.phone = phone
        self.email = email
        self.address = address
        self.pincode = pincode

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return '<User %r>' % self.name