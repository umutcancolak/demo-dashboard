from flask import jsonify
from flask_restful import Resource, reqparse
from .models import User, SensorInformationModel, FieldInformationModel
from .sensormodels import SensorModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

import pandas as pd

class Sensors(Resource):
    @jwt_required
    def get(self):

        # return jsonify({"message": [user.jsonify_all() for user in User.find_all()]})
        # return jsonify({"message": User.find_by_username("umutcan").jsonify_all()})
        sensor_data = SensorModel.find_last_n_data_by_id("2_1", n=20)
        
        return jsonify({
            "dates":[data["date"] for data in sensor_data],
            "moists":[data["moisture"] for data in sensor_data],
            "temps":[data["temperature"] for data in sensor_data]
            })
        # return jsonify({"data":SensorInformationModel.find_unique_ids_by_user_id(2)})

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

    @jwt_required
    def get(self, sensor_id):
        """
        Need to add specific sensor value here
        """
        # return jsonify(SensorModel.find_by_id(sensor_id))
        current_user = get_jwt_identity()
        return jsonify({"current_user":current_user})
    
    @jwt_required
    def post(self, sensor_id):
        data = Sensor.parser.parse_args()
        current_user_id = get_jwt_identity()
        if current_user_id != int(sensor_id.split("_")[0]):
            return {"message":"You are not authenticated to post by this token!"}, 401
        sensor_data = SensorModel(sensor_id, **data)
        try:
            sensor_data.save_to_mongo()
        except:
            return {"message":"There is a problem in Database!"}, 500
        return jsonify(sensor_data.jsonify())


        
