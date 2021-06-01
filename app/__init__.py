'''Autobase web
Website to control twitter_autobase bot
'''

__author__ = 'Fakhri Catur Rofi'
__license__ = 'Apache-2.0'
__version__ = '0.1'

from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

from . import routes, models, errors

from .auth import auth
app.register_blueprint(auth, url_prefix='/auth')
