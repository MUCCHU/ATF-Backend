from email import message
import email
from flask import jsonify
# from app import app
from unicodedata import name
from flask import request
from .models import Users
from .models import db
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import jwt

#Imports done

login_manager = LoginManager()
login_manager.session_protection = "strong"
def homepage():
    return {'message': 'Hello, world!'}, 200


def get_user(id: int):
    user = Users.query.filter_by(id=id).first()
    if user:
        return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        # user_model = Users()
        # user_model.id = user["id"]
        return user
    return None

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
        user = Users(name= data.get("name"), password= data.get("password"), phone=data.get("phone"), email=data.get("email"), address=None, pincode=None)
        db.session.add(user)
        print(user) 
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
            login_user(user)
            return jsonify({"message": "Login Success", "user": {"email": user.email, "name": user.name, "phone": user.phone}}), 200
            return {"message": "User signed in successfully" }, 200
        return {"message": "Invalid Credentials"}, 404

def check_session():
    if current_user.is_authenticated:
        return jsonify({"message": "User is logged in", "user": {"email": current_user.email, "name": current_user.name, "phone": current_user.phone}}), 200

    return jsonify({"message": "User is logged out"}), 404
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})
def queryusers():
    try:
        users = Users.query.all()
    except:
        return {"message": "Failed to get users"}, 500
    print("users = ",users)
    return str(users), 200