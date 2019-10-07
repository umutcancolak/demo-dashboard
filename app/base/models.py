from bcrypt import gensalt, hashpw, checkpw
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String
from ..mongo_db import Database
import datetime

from app import db, login_manager


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'password':
                value = hashpw(value.encode('utf8'), gensalt())
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def add_to_db(self):
        db.session.add(self)
        self.db_commit()

    def delete_from_db(self):
        db.session.delete(self)
        self.db_commit()

    def db_commit(self):
        db.session.commit()

    def hashpw(self, password):
        return hashpw(password.encode('utf8'), gensalt())

    def checkpw(self, password):
        return checkpw(password.encode('utf8'), self.password)


class SensorModel(object):
    def __init__(self, _id, moisture, temperature, date=datetime.datetime.now()):
        self._id = _id
        self.date = date
        self.moisture = moisture
        self.temperature = temperature       
    
    @staticmethod
    def get_all():
        return [result for result in Database.find("sensor_trial",{})]

    def save_to_mongo(self):
        Database.insert("sensor_trial",self.json())

    def json(self):
        return {
            "id": self._id,
            "date": self.date,
            "temperature": self.temperature,
            "moisture" : self.moisture
        }

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
