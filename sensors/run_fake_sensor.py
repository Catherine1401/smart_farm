import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.writer import write_to_cnosdb

def generate_data(station):
    return {
        "station": station,
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "soil_moisture": round(random.uniform(10, 60), 2)
    }

def write_data(station):
    data = generate_data(station)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {station} → {data}")

    measurement = "smart_farm"
    tags = f"station={data['station']}"
    fields = (
        f"temperature={data['temperature']},"
        f"humidity={data['humidity']},"
        f"soil_moisture={data['soil_moisture']}"
    )

    write_to_cnosdb(measurement, tags, fields)

def main():
    stations = [f"Field-{i+1}" for i in range(1000)]
    max_workers = 128

    while True:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(write_data, stations)
        time.sleep(1)

if __name__ == "__main__":
    main()
