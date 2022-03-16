from turtle import home
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Users
import views
from views import login_manager
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
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Harsh1606@localhost/users'
app.config.update(
    # DEBUG=True,
    # SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

# Routes
app.add_url_rule('/', view_func=views.homepage)
app.add_url_rule('/signup', methods=['POST'], view_func=views.signup)
app.add_url_rule('/signin', methods=['POST'], view_func=views.login)
app.add_url_rule('/check', methods=['POST'], view_func=views.check_session)
app.add_url_rule('/logout', methods=['POST'], view_func=views.logout)
app.add_url_rule('/queryusers', methods=['GET', 'POST'], view_func=views.queryusers)

