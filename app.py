from turtle import home
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Users
import views
from datetime import datetime
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'The secret is that IIT Kgp is an IIT :)'

db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Harsh1606@localhost/users'

# Routes
app.add_url_rule('/', view_func=views.homepage)
app.add_url_rule('/signup', methods=['POST'], view_func=views.signup)
app.add_url_rule('/signin', methods=['POST'], view_func=views.signin)
app.add_url_rule('/queryusers', methods=['GET', 'POST'], view_func=views.queryusers)

