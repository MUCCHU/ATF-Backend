from email import message
import email
from flask import jsonify
# from app import app
from unicodedata import name
from flask import request
from models import Users
from models import db
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
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
        user = Users(name= data.get("name"), password= data.get("password"), phone=data.get("phone"), email=data.get("email"), address=data.get("address"), pincode=int(data.get('pincode')))
        print(user)
        # try:
        db.session.add(user)
        db.session.commit()
        # print("Users = ",users);
        return {"message": "User signed up successfully" }, 201
        # except:
            # return {"message": "Failed to add new user" }, 500

def login():
    if request.method == 'POST':
        data = request.get_json()
        # print("data = ",data)
        user = Users.query.filter_by(email=data.get("email")).first()
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
            return jsonify({"login": True})
            return {"message": "User signed in successfully" }, 200
        return {"message": "Invalid Credentials"}, 404

def check_session():
    if current_user.is_authenticated:
        return jsonify({"login": True})

    return jsonify({"login": False})
def logout():
    logout_user()
    return jsonify({"logout": True})
def queryusers():
    users = Users.query.all()
    print("users = ",users)
    return str(users), 200