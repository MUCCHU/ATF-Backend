from re import X
from unicodedata import name
from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/delivery'
db=SQLAlchemy(app)
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Integer, nullable=False )
    

@app.route('/')
def ordertime():
    sample_name=['Alex smith','Raman mundol','Sunil patel','Dave kumar','Tom doe','James cook','John kk','himanshu sarkate','prabal sonakia','sonu kumar','pradipto mundol']
    name=random.choice(sample_name)
    time_of_preparation=random.randint(1,15)   
    time_to_reach=random.randint(1,15)
    time_to_deliver=random.randint(1,15)
    time=max(time_to_reach,time_of_preparation)+time_to_deliver
    order = Orders(name=name, time = time)
    db.session.add(order)
    db.session.commit()
    print(Orders.query.all())
    id=Orders.query[-1].id
    return {'name': name,'id': id,'time to reach':time_to_reach,'time of preparation':time_of_preparation,'time to deliver':time_to_deliver, 'total time': time, }







 

 