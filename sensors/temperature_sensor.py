# sensor/temperature_sensor.py

from sensors.base_sensor import BaseSensor
from datetime import datetime

class TemperatureSensor(BaseSensor):
    def generate_data(self):
        return {
            "time": datetime.utcnow().isoformat(),
            "station": self.get_station(),
            "temperature": self._random_value(20, 35)  # độ C
        }
