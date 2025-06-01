# sensor/humidity_sensor.py

from sensors.base_sensor import BaseSensor
from datetime import datetime

class HumiditySensor(BaseSensor):
    def generate_data(self):
        return {
            "time": datetime.utcnow().isoformat(),
            "station": self.get_station(),
            "humidity": self._random_value(40, 90)  # phần trăm
        }
