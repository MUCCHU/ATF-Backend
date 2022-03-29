from flask import request, jsonify
from models import *
from models import db
from functools import wraps
from flask import current_app as app
import jwt
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
            current_user = Users.query.filter_by(id = data['id']).first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated



def homepage():
    return {"message": "Hello World!"}, 200

# @token_required
def createorder():
    # print(current_user)
    data = request.get_json()
    order = Orders(status = "Processing", payment_mode = data['payment_mode'], delivery_address = data['delivery_address'])
    db.session.add(order)
    db.session.commit()
    return {"message": "Order Created"}, 201

def getorder():
    order = Orders.query.all()
    orderarr = []
    for i in order:
        orderarr.append(i.toDict())
    return {"orders": orderarr}, 200

def updateorder(id):
    data = request.get_json()
    order = Orders.query.filter_by(id = id).first()
    order.status = data['status']
    db.session.commit()
    return {"message": "Order Updated"}, 200

def deleteorder(id):
    # data = request.get_json()
    order = Orders.query.filter_by(id = id).first()
    db.session.delete(order)
    db.session.commit()
    return {"message": "Order Deleted"}, 200