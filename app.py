from flask import Flask
from flask_cors import CORS
from views import *
from datetime import datetime
from connection import connection, cursor

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'The secret is that IIT Kgp is an IIT :)'

# login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Harsh1606@localhost/orders'
app.config.update(
    # DEBUG=True,
    # SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
cors = CORS(
    app,
    resources={r"*": {"origins": "http://localhost:3000"}},
    expose_headers=["Content-Type", "X-CSRFToken"],
    supports_credentials=True,
)
# Routes
app.add_url_rule('/', view_func=homepage)
app.add_url_rule('/order/create', methods=['POST'], view_func=createorder)
app.add_url_rule('/order/get', methods=['GET'], view_func=getorder)
app.add_url_rule('/order/update/<id>', methods=['PUT'], view_func=updateorder)
app.add_url_rule('/order/delete/<id>', methods=['DELETE'], view_func=deleteorder)
app.add_url_rule('/order/<id>', methods = ['GET'], view_func=restaurant_menu)
# app.add_url_rule('/signin', methods=['POST'], view_func=login)
# app.add_url_rule('/check', methods=['POST'], view_func=check_session)
# app.add_url_rule('/logout', methods=['POST'], view_func=logout)
# app.add_url_rule('/queryusers', methods=['GET', 'POST'], view_func=queryusers)

