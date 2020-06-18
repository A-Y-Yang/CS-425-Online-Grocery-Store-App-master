from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from flask_bootstrap import Bootstrap
from shop.admin.forms import RegistrationForm, LoginForm, StaffRegistrationForm
#from shop.admin.models import Customer


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:1qaz2WSX3edc4RFV@cs425-aws-dbinstance.ctgzmkb6bvg8.us-east-2.rds.amazonaws.com/postgres'
app.config['SECRET_KEY'] = 'abcd1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#Bootstrap(app)

from shop.admin import routes