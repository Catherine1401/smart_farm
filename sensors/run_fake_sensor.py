import time
import random
from db.writer import write_to_cnosdb
from datetime import datetime

def generate_data(station):
    return {
        "station": station,
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "soil_moisture": round(random.uniform(10, 60), 2)
    }

def main():
    stations = [f"Field-{i+1}" for i in range(10)]
    while True:
        for station in stations:
            data = generate_data(station)
            print("Generated:", data)

            measurement = "smart_farm"
            tags = f"station={data['station']}"
            fields = f"temperature={data['temperature']},humidity={data['humidity']},soil_moisture={data['soil_moisture']}"

            write_to_cnosdb(measurement, tags, fields)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
