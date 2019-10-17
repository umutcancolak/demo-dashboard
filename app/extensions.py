from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .mongodb import Database
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
login_manager = LoginManager()
mongo_db = Database()
jwt = JWTManager()
