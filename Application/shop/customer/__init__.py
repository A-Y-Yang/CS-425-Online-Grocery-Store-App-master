from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from flask_bootstrap import Bootstrap
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres1@localhost/cs425'
app.config['SECRET_KEY'] = 'abcd1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#Bootstrap(app)

from shop.admin import routes
from shop.product import routes