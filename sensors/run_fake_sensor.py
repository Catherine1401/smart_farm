# sensor/generate_and_send.py

import time
from db.writer import write_to_cnosdb

from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.soil_sensor import SoilSensor

def main():
    stations = [f"Field-{i+1}" for i in range(10)]

    # Khởi tạo cảm biến cho mỗi vùng
    sensors = {
        station: {
            "temp": TemperatureSensor(station),
            "humid": HumiditySensor(station),
            "soil": SoilSensor(station)
        }
        for station in stations
    }

    while True:
        for station, sensor_dict in sensors.items():
            # Sinh dữ liệu từ từng cảm biến
            temp_data = sensor_dict["temp"].generate_data()
            humid_data = sensor_dict["humid"].generate_data()
            soil_data = sensor_dict["soil"].generate_data()

            # Gộp dữ liệu
            merged_data = {
                "station": station,
                "temperature": temp_data["temperature"],
                "humidity": humid_data["humidity"],
                "soil_moisture": soil_data["soil_moisture"]
            }

            print("Generated:", merged_data)

            # Ghi vào CNOSDB
            measurement = "smart_farm"
            tags = f"station={station}"
            fields = (
                f"temperature={merged_data['temperature']},"
                f"humidity={merged_data['humidity']},"
                f"soil_moisture={merged_data['soil_moisture']}"
            )

            write_to_cnosdb(measurement, tags, fields)

        time.sleep(1)

if __name__ == "__main__":
    main()
