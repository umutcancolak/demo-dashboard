from flask import jsonify
from flask_restful import Resource, reqparse

class Sensor(Resource):
    def get(self):
        return jsonify({"message": "Flask-Restfull worked succesfully"})