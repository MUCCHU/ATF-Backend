from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
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

@app.route('/add/<int:id1>/<int:creator1>/<type1>/<body1>/<banner1>')
def add(id1,creator1,type1,body1,banner1):
    now = datetime.now()
    usertobr=Notifs(id=id1,creator=creator1,type=type1,body=body1,banner=banner1,created_at=now,updated_at=now)
    db.session.add(usertobr)
    db.session.commit()
    return {"message":"hello"}

@app.route('/show')
def show():
    notifs=Notifs.query.all()
    for i in notifs:
         print(str(i.id)+' '+str(i.creator)+' '+i.type+' '+i.body+' '+i.banner+' '+i.created_at+' '+i.updated_at)
    print(notifs)
    return {"message":"hello"}

@app.route('/delete/<int:e>')
def dele(e):
    Notifs.query.filter_by(id=e).delete()
    db.session.commit()
    return {"message":"hello"}

@app.route('/update/<int:id1>/<int:creator1>/<type1>/<body1>/<banner1>')
def delcreate(id1,creator1,type1,body1,banner1):
    creatime=Notifs.query.filter_by(id=id1).first().created_at
    Notifs.query.filter_by(id=id1).delete()
    db.session.commit()
    now = datetime.now()
    usertobr=Notifs(id=id1,creator=creator1,type=type1,body=body1,banner=banner1,created_at=creatime,updated_at=now)
    db.session.add(usertobr)
    db.session.commit()
    return {"message":"hello"}


