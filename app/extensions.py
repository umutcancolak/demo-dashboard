from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .mongodb import Database

db = SQLAlchemy()
login_manager = LoginManager()
mongo_db = Database()
