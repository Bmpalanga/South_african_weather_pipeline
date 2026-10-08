import json
import pandas as pd
from pathlib import Path


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_weather_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def transform_weather_data():
    records = []

    for file_path in RAW_DIR.glob("*.json"):
        weather_data = load_weather_file(file_path)

        city = file_path.stem.rsplit("_", 2)[0]

        current = weather_data["current"]

        record = {
            "city": city,
            "timestamp": current["time"],
            "temperature_c": current["temperature_2m"],
            "humidity_percent": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"]
        }

        records.append(record)

    dataframe = pd.DataFrame(records)

    dataframe = dataframe.drop_duplicates(
        subset=["city", "timestamp"]
    )

    return dataframe.to_dict("records")
def save_processed_data(records):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(records)

    output_file = PROCESSED_DIR / "weather.csv"

    dataframe.to_csv(output_file, index=False)

    print(f"Saved processed data to: {output_file}")


def main():
    records = transform_weather_data()

    save_processed_data(records)


if __name__ == "__main__":
    main()