from ..mongodb import Database
import datetime

class SensorModel(object):
    def __init__(self, _id, moisture, temperature):
        self._id = _id
        self.date = datetime.datetime.now()
        self.moisture = moisture
        self.temperature = temperature       
    
    @staticmethod
    def get_all():
        return [result for result in Database.find({})]

    @staticmethod
    def find_by_id(sensor_id):
        return [data for data in Database.find({"id":sensor_id})]

    @staticmethod
    def find_last_n_data_by_id(sensor_id, n):
        return [data for data in Database.find({"id":sensor_id}).sort([("date",-1)]).limit(n)]

    @staticmethod
    def find_last_n_data_by_id_and_date(sensor_id, n, end , start):
        return [data for data in Database.find({"id":sensor_id, "date":{'$lte': end, '$gte': start}}).sort([("date",-1)]).limit(n)]

    def save_to_mongo(self):
        Database.insert(self.json())

    def json(self):
        """
        To return Json for database
        """
        return {
            "id": self._id,
            "date": self.date,
            "temperature": self.temperature,
            "moisture" : self.moisture
        }

    def jsonify(self):
        """
        To return Json as string
        """
        return {
            "id": self._id,
            "date": self.date.strftime("%m/%d/%Y, %H:%M:%S"),
            "temperature": self.temperature,
            "moisture" : self.moisture
        }