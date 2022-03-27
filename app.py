from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request
from datetime import datetime

engine = create_engine('mysql://root:hello@localhost/notifications', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


from sqlalchemy.orm import relationship, backref

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hello@localhost/notifications'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

class Notifs(db.Model):
    __table__ = db.Model.metadata.tables['notifications']

@app.route('/add', methods=['POST'])
def add():
    id = request.values.get("id")
    creator = request.values.get("creator")
    type=request.values.get("type")
    body=   request.values.get("body")
    banner=   request.values.get("banner")
    now = datetime.now()
    usertobr=Notifs(id=id,creator=creator,type=type,body=body,banner=banner,created_at=now,updated_at=now)
    db.session.add(usertobr)
    db.session.commit()
    return "VALUES ADDED"

@app.route('/show', methods=['GET','POST'])
def ind():
    id = request.values.get('id')
    print(str(Notifs.query.filter_by(id=id).first().id)+' '+str(Notifs.query.filter_by(id=id).first().creator)+' '+str(Notifs.query.filter_by(id=id).first().type)+' '+str(Notifs.query.filter_by(id=id).first().body)+' '+str(Notifs.query.filter_by(id=id).first().banner)+' '+str(Notifs.query.filter_by(id=id).first().created_at)+' '+str(Notifs.query.filter_by(id=id).first().updated_at)+' ')
    return (str(Notifs.query.filter_by(id=id).first().id)+' '+str(Notifs.query.filter_by(id=id).first().creator)+' '+str(Notifs.query.filter_by(id=id).first().type)+' '+str(Notifs.query.filter_by(id=id).first().body)+' '+str(Notifs.query.filter_by(id=id).first().banner)+' '+str(Notifs.query.filter_by(id=id).first().created_at)+' '+str(Notifs.query.filter_by(id=id).first().updated_at)+' ')


@app.route('/', methods=['GET'])
def index():
    notifs=Notifs.query.all()
    for i in notifs:
         print(str(i.id)+' '+str(i.creator)+' '+i.type+' '+i.body+' '+i.banner+' '+str(i.created_at)+' '+str(i.updated_at))
    return "VALUES PRINTED"

@app.route('/delete', methods=['DELETE'])
def dele():
    id = request.values.get('id')
    Notifs.query.filter_by(id=id).delete()
    db.session.commit()
    return "VALUES DELETED"

@app.route('/update', methods=['PUT'])
def delcreate():
    id = request.values.get('id')
    creator = request.values.get('creator')
    type = request.values.get('type')
    body = request.values.get('body')
    banner = request.values.get('banner')
    creatime=Notifs.query.filter_by(id=id).first().created_at
    Notifs.query.filter_by(id=id).delete()
    db.session.commit()
    now = datetime.now()
    usertobr=Notifs(id=id,creator=creator,type=type,body=body,banner=banner,created_at=creatime,updated_at=now)
    db.session.add(usertobr)
    db.session.commit()
    return "VALUES UPDATED"



