from email import message
import email
from flask import jsonify, make_response
# from app import app
from datetime import datetime, timedelta
from flask import current_app as app
from unicodedata import name
from flask import request
from .models import Restaurants, Users
from .models import db
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )
import jwt

#Imports done

# login_manager = LoginManager()
# login_manager.session_protection = "strong"
def homepage():
    return {'message': 'Hello, world!'}, 200


def get_user(id: int):
    user = Users.query.filter_by(id=id).first()
    if user:
        return user
    return None


# @login_manager.user_loader
# def user_loader(id: int):
#     user = get_user(id)
#     if user:
#         # user_model = Users()
#         # user_model.id = user["id"]
#         return user
#     return None

def signup():
    if request.method == 'POST':
        # print("request ka data",request)
        data = request.get_json()
        print("pincode - ",data.get('pincode'))
        # users = Users.query.all()
        # try:
        userd = Users.query.filter_by(email=data.get("email")).first()
        if userd:
            return jsonify({"message": "Email already exists"}), 400
        if data.get('is_restaurant'):
            user = Users(name= data.get("name"), password= data.get("password"), phone=data.get("phone"), email=data.get("email"), address=None, pincode=None, is_restaurant= True)
            restaurant = Restaurants(user=user, opening_time= data.get("opening_time"), closing_time= data.get("closing_time"))
            db.session.add(user)
            db.session.add(restaurant)
            db.session.commit()
            print(user) 
            # db.session.commit()
        else:
            user = Users(name= data.get("name"), password= data.get("password"), phone=data.get("phone"), email=data.get("email"), address=None, pincode=None, is_restaurant= False)
            db.session.add(user)
            # db.session.add(restaurant)
            db.session.commit()
        # except:
        #     return {"message": "Failed to signup"}, 500
        # try:
        # print("Users = ",users);
        return {"message": "User signed up successfully" }, 201
        # except:
            # return {"message": "Failed to add new user" }, 500

def login():
    if request.method == 'POST':
        data = request.get_json()
        # print("data = ",data)
        try: 
            user = Users.query.filter_by(email=data.get("email")).first()
        except:
            print("Databse Error")
            return {"message": "Failed to login"}, 500
        # users = Users.query.all()
        # for user in users:
        #     print("user email = ",user.email)
        if user is None:
            return {"message": "Invalid Credentials"}, 404

        print("user = ",user)
        if user.check_password(data.get("password")):
            # user_model = Users()
            # Users.id = user["id"]
            token = jwt.encode({
            'id': user.id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
            # login_user(user)
            res = make_response(jsonify({"message": "Logged in successfully"}), 200)
            res.set_cookie("token", token.decode('UTF-8'), httponly=True, samesite='None', secure=True, expires=datetime.utcnow() + timedelta(days= 1))
            res.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')
            return res
            # return jsonify({"message": "Login Success","user": {"email": user.email, "name": user.name, "phone": user.phone}}), 200
            # return {"message": "User signed in successfully" }, 200
        return {"message": "Invalid Credentials"}, 404

def check_session():

    token = request.cookies.get('token')
    if token:
        print(token)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return {"message": "Failed to get users"}, 500
        # print("data = ",data)
        user = get_user(data['id'])
        if user:
            return {"message": "User is authenticated", "user": {"email": user.email, "name": user.name, "phone": user.phone}}, 200
        return {"message": "User not authenticated"}, 404
    # if current_user.is_authenticated:
    #     return jsonify({"message": "User is logged in", "user": {"email": current_user.email, "name": current_user.name, "phone": current_user.phone}}), 200

    return jsonify({"message": "User is logged out"}), 404
def logout():
    resp = make_response(jsonify({"message": "User logged out"}), 200)
    resp.set_cookie('token', '', expires=0)
    return resp
    # logout_user()
    # return jsonify({"message": "Logged out successfully"})
def queryusers():
    try:
        users = Users.query.all()
    except:
        return {"message": "Failed to get users"}, 500
    print("users = ",users)
    for user in users:
        print("name = ",user.name)
        print("password = ", user.password)
        print("phone = ", user.phone)
        print("email = ", user.email)
        print("address =", user.address)
        print("pincode = ", user.pincode)
        print("is_restaurent = ", user.is_restaurant)
        print("created_at = ", user.created_at)
        print("updated_at = ", user.updated_at)
        print("last_login_at = ", user.last_login_at)
        if user.is_restaurant:
            print('User.rest=', user.restaurant)
            print("opening_time = ", user.restaurant.opening_time)
            print("closing_time = ", user.restaurant.closing_time)
    return str(users), 200