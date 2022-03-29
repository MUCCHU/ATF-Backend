from flask import jsonify, make_response
from datetime import datetime, timedelta
from flask import current_app as app
from unicodedata import name
from flask import request
from pymysql import NULL
from werkzeug.security import generate_password_hash, check_password_hash
from .connection import connection, cursor
import jwt
def homepage():
    return {'message': 'Hello, world!'}, 200
def get_user(id: int):
    cursor.execute('SELECT * FROM users WHERE user_id = %s;', (id,))
    user = cursor.fetchone()
    if user:
        return user
    return None
def signup():
    if request.method == 'POST':
        data = request.get_json()
        print("pincode - ",data.get('pincode'))
        try: 
            cursor.execute('SELECT * FROM users WHERE email = %s;', (data.get("email"),))
        except:
            print("Databse Error")
            return {"message": "Failed to Singup"}, 500
        if cursor.fetchone():
            return {"message": "Email already exists"}, 400
        uname = data.get("name")
        email = data.get("email")
        mobile = int(data.get("phone"))
        address = data.get("address")
        pincode = int(data.get("pincode"))
        passwd = generate_password_hash(data.get("password"))

        try:
            cursor.execute('INSERT INTO users (uname, passwd, mobile, email, address, pincode, loyalty_pts, created_on, updated_on, last_login) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (uname, passwd, mobile, email, address, pincode, 0, datetime.now(), NULL, NULL))
            connection.commit()
            return {"message": "User signed up successfully" }, 201
        except:
            return {"message": "Failed to add new user" }, 500

def login():
    if request.method == 'POST':
        data = request.get_json()
        user = None
        try: 
            cursor.execute('SELECT * FROM users WHERE email = %s;', (data.get("email"),))
        except:
            print("Databse Error")
            return {"message": "Failed to login"}, 500
        user = cursor.fetchone()
        if user is None:
            return {"message": "Invalid Credentials"}, 404
        if check_password_hash(user[2], data.get("password")):
            token = jwt.encode({
            'id': user[0],
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
            res = make_response(jsonify({"message": "Logged in successfully"}), 200)
            res.set_cookie("token", token.decode('UTF-8'), httponly=True, samesite='None', secure=True, expires=datetime.utcnow() + timedelta(days= 1))
            res.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')
            return res
        return {"message": "Invalid Credentials"}, 404

def check_session():

    token = request.cookies.get('token')
    if token:
        print(token)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return {"message": "Failed to get users"}, 500
        user = get_user(data['id'])
        if user:
            print("user = ",user)
            return {"message": "User is authenticated", "user": {"email": user[4], "name": user[1], "phone": user[3]}}, 200
        return {"message": "User not authenticated"}, 404

    return jsonify({"message": "User is logged out"}), 404
def logout():
    resp = make_response(jsonify({"message": "User logged out"}), 200)
    resp.set_cookie('token', '', expires=0)
    return resp