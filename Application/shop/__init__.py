from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_login import LoginManager
#from flask_bootstrap import Bootstrap
import os
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master:cs425!ProjectGroup3@cs425-ogs-group-3.cnjzlkxau3i8.us-east-1.rds.amazonaws.com/cs425'
app.config['SECRET_KEY'] = 'abcd1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#Bootstrap(app)
#search = Seach()
#search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "postgresql":
        migrate.init_app(app, db, render_as_batch = True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customer_login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_messgae = u"Please login first"

from shop.admin import routes
from shop.product import routes
from shop.customer import routes
from shop.cart import carts