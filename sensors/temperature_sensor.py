# sensor/temperature_sensor.py

from sensors.base_sensor import BaseSensor
from datetime import datetime
import random

class TemperatureSensor(BaseSensor):
    def __init__(self, station):
        super().__init__(station)
        self.current_temp = random.uniform(25, 30)  # giá trị ban đầu hợp lý

    def generate_data(self):
        # Biến thiên nhỏ ±0.5°C mỗi lần
        delta = random.uniform(-0.5, 0.5)
        self.current_temp += delta

        # Giới hạn trong khoảng an toàn (20 - 35°C)
        self.current_temp = max(20, min(35, self.current_temp))

        return {
            "time": datetime.utcnow().isoformat(),
            "station": self.get_station(),
            "temperature": round(self.current_temp, 2)
        }
