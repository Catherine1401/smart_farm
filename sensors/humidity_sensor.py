# sensor/humidity_sensor.py

from sensors.base_sensor import BaseSensor
from datetime import datetime
import random

class HumiditySensor(BaseSensor):
    def __init__(self, station):
        super().__init__(station)
        self.current_humidity = random.uniform(50, 80)  # giá trị khởi đầu hợp lý

    def generate_data(self):
        # Dao động ±3% mỗi lần
        delta = random.uniform(-0.05, 0.05)
        self.current_humidity += delta

        # Giữ trong khoảng 40% - 90%
        self.current_humidity = max(40, min(90, self.current_humidity))

        return {
            "time": datetime.utcnow().isoformat(),
            "station": self.get_station(),
            "humidity": round(self.current_humidity, 2)
        }
