import urllib.request
import os
import kagglehub
import shutil

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "processed"), exist_ok=True)

print(f"Downloading data to {RAW_DATA_DIR}...")

# 1. NYC TLC Yellow Taxi (Jan 2024)
taxi_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
taxi_path = os.path.join(RAW_DATA_DIR, "yellow_tripdata_2024-01.parquet")
if not os.path.exists(taxi_path):
    print("Downloading NYC TLC Yellow Taxi data...")
    urllib.request.urlretrieve(taxi_url, taxi_path)
    print("Taxi data downloaded.")
else:
    print("Taxi data already exists.")

# 2. Taxi Zone Lookup
zone_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
zone_path = os.path.join(RAW_DATA_DIR, "taxi_zone_lookup.csv")
if not os.path.exists(zone_path):
    print("Downloading Taxi Zone Lookup...")
    urllib.request.urlretrieve(zone_url, zone_path)
    print("Taxi Zone Lookup downloaded.")
else:
    print("Taxi Zone Lookup already exists.")

# 3. NOAA Weather (Using Open-Meteo Archive API for NYC Jan 2024)
# Central Park coords: 40.7831, -73.9712
weather_url = "https://archive-api.open-meteo.com/v1/archive?latitude=40.7831&longitude=-73.9712&start_date=2024-01-01&end_date=2024-01-31&hourly=temperature_2m,precipitation,wind_speed_10m&format=csv"
weather_path = os.path.join(RAW_DATA_DIR, "nyc_weather_2024-01.csv")
if not os.path.exists(weather_path):
    print("Downloading NYC Weather data...")
    urllib.request.urlretrieve(weather_url, weather_path)
    print("Weather data downloaded.")
else:
    print("Weather data already exists.")

# 4. NYC Housing Market Data (Kaggle)
housing_dest = os.path.join(RAW_DATA_DIR, "nyc_housing_market.csv")
if not os.path.exists(housing_dest):
    print("Downloading NYC Housing Market data via kagglehub...")
    try:
        path = kagglehub.dataset_download("nelgiriyewithana/new-york-housing-market")
        # Find the CSV in the downloaded path
        for file in os.listdir(path):
            if file.endswith(".csv"):
                shutil.copy(os.path.join(path, file), housing_dest)
                print("Housing Market data copied to raw folder.")
                break
    except Exception as e:
        print(f"Failed to download housing data (ensure kagglehub is installed): {e}")
else:
    print("Housing data already exists.")

print("All downloads complete!")
