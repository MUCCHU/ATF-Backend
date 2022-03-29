from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect


# from numpy import product
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    is_restaurant = db.Column(db.Boolean, nullable=False, default=False)
    restaurant = db.relationship('Restaurants', backref='user', uselist = False)
    order = db.relationship('Orders', backref='user', uselist = False)
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
    items = db.relationship('Items', backref='restaurant')
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

class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=True)
    discount_rate = db.Column(db.Integer, nullable=True)
    discount_type = db.Column(db.String(10), nullable=True)
    coupoun_code = db.Column(db.String(10), nullable=True)
    loyalty_threshold = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    remark = db.Column(db.String(200), nullable=True)


class Product(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    item = db.relationship('Items', backref='product')
    is_available = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.id'))
    restaurantid = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    productid = db.Column(db.Integer, db.ForeignKey('product.id'))
    offerid = db.Column(db.Integer, db.ForeignKey('offers.id'))
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# @dataclass
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(50), nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False)
    delivery_address = db.Column(db.String(200), nullable=True)
    items = db.relationship('Items', backref='order', uselist = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Order %r>' % self.id
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }




