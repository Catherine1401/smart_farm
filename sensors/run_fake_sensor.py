# sensor/generate_and_send.py

import time
import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from db.writer import write_to_cnosdb, batch_write_to_cnosdb
from concurrent.futures import ThreadPoolExecutor
import random

from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.soil_sensor import SoilSensor

def generate_zone_data(station):
    """Generate data for a single zone"""
    sensors = {
        "temp": TemperatureSensor(station),
        "humid": HumiditySensor(station),
        "soil": SoilSensor(station)
    }
    
    # Generate data from each sensor
    temp_data = sensors["temp"].generate_data()
    humid_data = sensors["humid"].generate_data()
    soil_data = sensors["soil"].generate_data()

    # Merge data
    merged_data = {
        "station": station,
        "temperature": temp_data["temperature"],
        "humidity": humid_data["humidity"],
        "soil_moisture": soil_data["soil_moisture"]
    }

    # Prepare line protocol data
    measurement = "smart_farm"
    tags = f"station={station}"
    fields = (
        f"temperature={merged_data['temperature']},"
        f"humidity={merged_data['humidity']},"
        f"soil_moisture={merged_data['soil_moisture']}"
    )

    return measurement, tags, fields

def main():
    # Create 1000 zones
    stations = [f"Field-{i+1:04d}" for i in range(1000)]
    
    # Number of worker threads for parallel processing
    max_workers = 10
    
    print(f"Starting sensor simulation for {len(stations)} zones...")
    
    while True:
        start_time = time.time()
        data_points = []
        
        # Process zones in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all zone data generation tasks
            future_to_station = {
                executor.submit(generate_zone_data, station): station 
                for station in stations
            }
            
            # Collect results
            for future in future_to_station:
                try:
                    data_point = future.result()
                    data_points.append(data_point)
                except Exception as e:
                    print(f"Error processing zone {future_to_station[future]}: {e}")
        
        # Write data in batches
        if data_points:
            batch_write_to_cnosdb(data_points, batch_size=100)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        print(f"Processed {len(stations)} zones in {processing_time:.2f} seconds")
        
        # Sleep to maintain desired update frequency
        if processing_time < 1.0:
            time.sleep(1.0 - processing_time)

if __name__ == "__main__":
    main()
