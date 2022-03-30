from flask import jsonify, make_response
from datetime import datetime, timedelta
from flask import current_app as app
from unicodedata import name
from flask import request
from pymysql import NULL
from werkzeug.security import generate_password_hash, check_password_hash
from .connection import connection, cursor
import jwt
import json
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
            'is_restaurant': False,
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
        if data['is_restaurant']:
            print("it is restaurant")
            cursor.execute('SELECT * FROM restaurants WHERE restaurant_id = %s;', (data["id"],))
            restaurant = cursor.fetchone()
            return json.dumps({"message": "Restaurant is authenticated", "user": {"id":restaurant[0], "email": restaurant[3], "name": restaurant[1], "phone": restaurant[5], "address": restaurant[4], "pincode": restaurant[6], "open_time":restaurant[7], "close_time": restaurant[8], "is_open": restaurant[9]}},indent=4, sort_keys=True, default=str)
            # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
        else:
            user = get_user(data['id'])
            if user:
                print("user = ",user)
                return {"message": "User is authenticated", "restuarant": {"id": user[0], "email": user[4], "name": user[1], "phone": user[3]}}, 200
            return {"message": "User not authenticated"}, 404

    return jsonify({"message": "User is logged out"}), 404
def logout():
    resp = make_response(jsonify({"message": "User logged out"}), 200)
    resp.set_cookie('token', '', expires=0)
    return resp

def signup_restaurant():
        data = request.get_json()
        print("pincode - ",data.get('pincode'))
        # try: 
        cursor.execute('SELECT * FROM restaurants WHERE email = %s;', (data.get("email"),))
        # except:
        #     print("Databse Error")
        #     return {"message": "Failed to Singup"}, 500
        if cursor.fetchone():
            return {"message": "Email already exists"}, 400
        uname = data.get("name")
        email = data.get("email")
        mobile = int(data.get("phone"))
        address = data.get("address")
        pincode = int(data.get("pincode"))
        open_time = data.get("open_time")
        close_time = data.get("close_time")
        is_open = True
        passwd = generate_password_hash(data.get("password"))

        try:
            cursor.execute('INSERT INTO restaurants (r_name, passwd, email, mobile, address, pincode, open_time, close_time, is_open) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s);', (uname, passwd, email, mobile, address, pincode, open_time, close_time, is_open))
            connection.commit()
            return {"message": "Restaurant signed up successfully" }, 201
        except:
            return {"message": "Failed to add new user" }, 500

def login_restaurant():
    # if request.method == 'POST':
        data = request.get_json()
        restaurant = None
        try: 
            cursor.execute('SELECT * FROM restaurants WHERE email = %s;', (data.get("email"),))
        except:
            print("Databse Error")
            return {"message": "Failed to login"}, 500
        restaurant = cursor.fetchone()
        if restaurant is None:
            return {"message": "Invalid Credentials"}, 404
        if check_password_hash(restaurant[2], data.get("password")):
            token = jwt.encode({
            'id': restaurant[0],
            'is_restaurant': True,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
            res = make_response(jsonify({"message": "Restaurant Logged in successfully"}), 200)
            res.set_cookie("token", token.decode('UTF-8'), httponly=True, samesite='None', secure=True, expires=datetime.utcnow() + timedelta(days= 1))
            res.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')
            return res
        return {"message": "Invalid Credentials"}, 404