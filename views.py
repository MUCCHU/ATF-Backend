from email import message
import email
from unicodedata import name
from flask import request
from models import Users
from models import db
def homepage():
    return {'message': 'Hello, world!'}, 200


def signup():
    if request.method == 'POST':
        # print("request ka data",request)
        data = request.get_json()
        print("pincode - ",data.get('pincode'))
        users = Users.query.all()
        user = Users(name= data.get("name"), password= data.get("password"), phone=data.get("phone"), email=data.get("email"), address=data.get("address"), pincode=int(data.get('pincode')))
        print(user)
        # try:
        db.session.add(user)
        db.session.commit()
        print("Users = ",users);
        return {"message": "User signed up successfully" }, 201
        # except:
            # return {"message": "Failed to add new user" }, 500

def signin():
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
            return {"message": "User signed in successfully" }, 200
        return {"message": "Invalid Credentials"}, 404


def queryusers():
    users = Users.query.all()
    print("users = ",users)
    return str(users), 200