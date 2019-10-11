from flask import jsonify
from flask_restful import Resource, reqparse
from .models import User, SensorInformationModel, FieldInformationModel
from .sensormodels import SensorModel

class Sensors(Resource):
    def get(self):
        # return jsonify({"message": [user.jsonify_all() for user in User.find_all()]})
        # return jsonify({"message": User.find_by_username("umutcan").jsonify_all()})
        return jsonify({"data":SensorModel.get_all()})

class Sensor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("moisture",
        type = float,
        required = True,
        help = "This field can not be left blank"
    )
    parser.add_argument("temperature",
        type =float,
        required = True,
        help = "This field can not be left blank"
    )
    def get(self, sensor_id):
        return jsonify(SensorModel.find_by_id(sensor_id))
    
    def post(self, sensor_id):
        data = Sensor.parser.parse_args()
        sensor_data = SensorModel(sensor_id, **data)
        try:
            sensor_data.save_to_mongo()
        except:
            return jsonify({"message":"There is a problem in Database!"})
        return jsonify(sensor_data.jsonify())


        
