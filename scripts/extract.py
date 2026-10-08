import json
import requests
from datetime import datetime
from pathlib import Path


CONFIG_FILE = "config/config.json"
OUTPUT_DIR = Path("data/raw")

API_URL = "https://api.open-meteo.com/v1/forecast"


def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def fetch_weather(city, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Failed to get weather for {city}: {error}")
        return None


def save_raw_data(city, weather_data):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{city.replace(' ', '_').lower()}_{timestamp}.json"

    output_file = OUTPUT_DIR / filename

    with open(output_file, "w") as file:
        json.dump(weather_data, file, indent=4)

    print(f"Saved: {output_file}")


def main():
    config = load_config()

    cities = config["cities"]

    for city, coordinates in cities.items():

        print(f"Getting weather for {city}...")

        weather_data = fetch_weather(
            city,
            coordinates["latitude"],
            coordinates["longitude"]
        )
        if weather_data is not None:

          save_raw_data(city, weather_data)


if __name__ == "__main__":
    main()