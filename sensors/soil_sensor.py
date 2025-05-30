# sensor/soil_sensor.py

from sensors.base_sensor import BaseSensor
from datetime import datetime
import random

class SoilSensor(BaseSensor):
    def __init__(self, station):
        super().__init__(station)
        self.current_soil = random.uniform(30, 50)  # giá trị khởi đầu hợp lý

    def generate_data(self):
        # Dao động nhẹ mỗi lần ±2%
        delta = random.uniform(-0.05, 0.05)
        self.current_soil += delta

        # Giới hạn trong khoảng an toàn (10% - 60%)
        self.current_soil = max(10, min(60, self.current_soil))

        return {
            "time": datetime.utcnow().isoformat(),
            "station": self.get_station(),
            "soil_moisture": round(self.current_soil, 2)
        }
