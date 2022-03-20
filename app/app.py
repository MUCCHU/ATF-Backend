# from turtle import home
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from .models import db
from .models import Users
from flask_cors import CORS
from .views import *
# from .views import login_manager
from datetime import datetime
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'The secret is that IIT Kgp is an IIT :)'

db.init_app(app)
# login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6480330:VxdvywzzhL@sql6.freemysqlhosting.net/sql6480330'
app.config.update(
    # DEBUG=True,
    # SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
cors = CORS(
    app,
    resources={r"*": {"origins": "http://localhost:8080"}},
    expose_headers=["Content-Type", "X-CSRFToken"],
    supports_credentials=True,
)
# Routes
app.add_url_rule('/', view_func=homepage)
app.add_url_rule('/signup', methods=['POST'], view_func=signup)
app.add_url_rule('/signin', methods=['POST'], view_func=login)
app.add_url_rule('/check', methods=['POST'], view_func=check_session)
app.add_url_rule('/logout', methods=['POST'], view_func=logout)
app.add_url_rule('/queryusers', methods=['GET', 'POST'], view_func=queryusers)

