# sensor/soil_sensor.py

from sensors.base_sensor import BaseSensor
from datetime import datetime

class SoilSensor(BaseSensor):
    def generate_data(self):
        return {
            "time": datetime.utcnow().isoformat(),
            "station": self.get_station(),
            "soil_moisture": self._random_value(10, 60)  # phần trăm
        }
