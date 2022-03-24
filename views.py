from flask import request, jsonify
from models import *
from models import db
def homepage():
    return {"message": "Hello World!"}, 200
def createorder():
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