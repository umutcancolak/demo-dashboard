from flask import jsonify
from flask_restful import Resource, reqparse
from .models import User, SensorInformationModel, FieldInformationModel

class Sensor(Resource):
    def get(self):
        return jsonify({"message": [user.jsonify_all() for user in User.find_all()]})
