from flask import request, jsonify
from functools import wraps
from flask import current_app as app
import jwt
import indian_names as names
from connection import connection, cursor
import random
# from models import Users

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        token = request.cookies.get('token')
        if 'token' in request.cookies.keys():
            token = request.cookies.get('token')
            print(token)
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            print(app.config['SECRET_KEY'])
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            cursor.execute("SELECT * FROM users WHERE user_id = %s;", (data["id"],))
            # Handle error if no such user exists
            feedbacks = []
            for feedback in cursor:
                feedbacks.append(feedback)
            current_user = feedbacks[0]
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated



def homepage():
    return {"message": "Hello World!"}, 200

@token_required
def createorder(user):
    user_id = user[0]
    delivery_address = user[5]+', '+str(user[6])
    data = request.get_json()
    time_for_preparation=random.randint(1,15)   
    time_to_reach=random.randint(1,15)
    time_to_deliver=random.randint(1,15)
    total_time=max(time_to_reach,time_for_preparation)+time_to_deliver
    cursor.execute(
        "INSERT INTO orders (user_id, delivery_agent_name, time_for_preparation, time_to_reach, time_to_deliver, total_time, delivery_address, payment_mode, ordered_on) VALUES (?,?,?,?,?,?,?,?,?);",
        (user_id, names.get_full_name(gender='male'), time_for_preparation, time_to_reach, time_to_deliver, total_time, delivery_address, data["payment_mode"], NOW()) )
    return {"message": "Order Created"}, 201


def getorder():
    cursor.execute("SELECT * FROM orders")
    orders = []
    for feedback in cursor:
        orders.append(feedback)
    return {"orders": orders}, 200

def updateorder(id):
    data = request.get_json()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (data["status"], id,))
    return {"message": "Order Updated"}, 200

def deleteorder(id):
    # data = request.get_json()
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (id,))
    return {"message": "Order Deleted"}, 200