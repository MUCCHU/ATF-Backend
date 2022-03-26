# from app import db
from collections import UserList
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# import jwt
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)


engine = create_engine('mysql://opensoft:opensoft@opensoft-1.cwvqdtxsixl6.ap-south-1.rds.amazonaws.com/opensoft', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


db = SQLAlchemy()
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    is_restaurant = db.Column(db.Boolean, nullable=False, default=False)
    restaurant = db.relationship('Restaurants', backref='user', uselist = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, password, phone, email, address, pincode, is_restaurant):
        self.name = name
        self.password = generate_password_hash(password,method='pbkdf2:sha256', salt_length=8)
        self.phone = phone
        self.email = email
        self.address = address
        self.pincode = pincode
        self.is_restaurant = is_restaurant
        # if is_restaurant:
        #     self.resataurant = Restaurants(opening_time = opening_time, closing_time = closing_time)
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return '<User %r>' % self.name

class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=True)
    # def __init__(self, name, phone, email, address, pincode):
    #     self.name = name
    #     self.phone = phone
    #     self.email = email
    #     self.address = address
    #     self.pincode = pincode

    def __repr__(self):
        return '<Restaurant %r>' % self.user.name