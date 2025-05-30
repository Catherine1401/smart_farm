# sensor/base_sensor.py

from abc import ABC, abstractmethod
import random
import time
from typing import Dict, Any

class BaseSensor(ABC):
    def __init__(self, station: str):
        self.station = station

    @abstractmethod
    def generate_data(self) -> Dict[str, Any]:
        """Tạo một bản ghi dữ liệu cảm biến"""
        pass

    def _random_value(self, min_val: float, max_val: float) -> float:
        return round(random.uniform(min_val, max_val), 2)

    def get_station(self) -> str:
        return self.station
