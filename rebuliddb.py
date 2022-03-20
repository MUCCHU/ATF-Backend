#!./env/bin/python
from app.models import db
from app.app import app
with app.app_context():
    db.create_all()