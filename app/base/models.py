from bcrypt import gensalt, hashpw, checkpw
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey
import datetime

from app import db, login_manager


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    field_info = db.relationship("FieldInformationModel",lazy = "dynamic")
    sensor_info = db.relationship("SensorInformationModel",lazy = "dynamic") 

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

    def json(self):
        return {
            "user_id" : self.id,
            "username" : self.username,
            "e-mail" : self.email
        }

    def jsonify_all(self):
        return {
            "user_id" : self.id,
            "username" : self.username,
            "e-mail" : self.email,
            "field_info" : [field.json() for field in self.field_info.all()],
            "sensor_info": [sensor.json() for sensor in self.sensor_info.all()]
        }

    def jsonify_fields(self):
        return {"fields_info" : [field.json() for field in self.field_info.all()]}

    def jsonify_sensors(self):
        return {"sensor_info": [sensor.json() for sensor in self.sensor_info.all()]}
        
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
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class FieldInformationModel(db.Model):
    __tablename__ = "field_info"

    _id = Column(Integer,primary_key = True)
    field_name = Column(String(80))
    user_id = Column(Integer, ForeignKey('User.id'))

    def __init__(self , user_id , field_name):
        self.user_id = user_id
        self.field_name = field_name

    def json(self):
        return {
            "field_id": self._id,
            "user_id" : self.user_id,
            "field_name" : self.field_name
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_user_id_and_field_name(cls, user_id , field_name):
        return cls.query.filter_by(user_id = user_id , field_name = field_name ).first()




class SensorInformationModel(db.Model):
    __tablename__ = "sensors_info"

    _id = Column(Integer,primary_key = True)
    sensor_type = Column(String(80))
    user_id = Column(Integer, ForeignKey('User.id'))
    field_name = Column(String(80))


    # users = db.relationship('UserModel')

    def __init__(self, user_id, field_name , sensor_type):
        self.user_id = user_id
        self.field_name = field_name
        self.sensor_type = sensor_type
        
          
    def json(self):
        return {
            "user_id":self.user_id,
            "sensor_id":self._id,
            "field_name" :self.field_name,
            "sensor_name":self.sensor_type,
            "sensor_unique_id" : self.get_device_id()
        }         

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_field(self, new_field):
        self.field_name = new_field
        db.session.commit()

    def get_device_id(self, jsonify = False):
        if jsonify :
            return {"sensor_unique_id":str(self.user_id) + "0" + str(self._id)} 
        else:
            return "{}_{}".format(self.user_id,self._id)

    @classmethod
    def find_by_user_id_and_sensor_type(cls, user_id , sensor_type):
        return cls.query.filter_by(user_id = user_id , sensor_type = sensor_type ).first()
    
    @classmethod
    def find_by_user_id_and_sensor_id(cls, user_id , _id):
        return cls.query.filter_by(user_id = user_id , _id = _id).first()

    @classmethod
    def find_by_field_name_and_sensor_type(cls, field_name , sensor_type):
        return cls.query.filter_by(field_name = field_name , sensor_type = sensor_type ).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_unique_ids(cls):
        return [user.json()["sensor_unique_id"] for user in cls.find_all()]

    @classmethod
    def find_unique_ids_by_user_id(cls, user_id):
        return [user.json()["sensor_unique_id"] for user in cls.find_all() if user.json()["user_id"] == user_id]