from flask import jsonify
from flask_restful import Resource, reqparse
from .models import User
import pandas as pd

class Sensor(Resource):
    def get(self):
        return jsonify({"message": [user.json() for user in User.find_all()]})