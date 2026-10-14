import json
import pandas as pd
from pathlib import Path


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_weather_file(file_path):
    """
    Load weather data from a JSON file.

    Returns the loaded data if successful.
    Returns None if the file is invalid or cannot be read.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON file: {file_path}")
        return None

    except OSError as error:
        print(f"Warning: Could not read {file_path}: {error}")
        return None


def transform_weather_data():
    """
    Read raw weather JSON files, validate the data,
    remove duplicate records, and return clean records.
    """
    records = []

    for file_path in RAW_DIR.glob("*.json"):

        # Load the JSON file
        weather_data = load_weather_file(file_path)

        # Skip files that could not be loaded
        if weather_data is None:
            continue

        #  Determine the city from the filename
        city = file_path.stem.rsplit("_", 2)[0]

        #  Validate the overall API response
        if not isinstance(weather_data, dict):
            print(
                f"Warning: Invalid API response for {city}. "
                "Skipping record."
            )
            continue

        # Check that the current section exists
        if "current" not in weather_data:
            print(
                f"Warning: Missing current weather data for {city}. "
                "Skipping record."
            )
            continue

        current = weather_data["current"]

        #  Validate the current weather section
        if not isinstance(current, dict):
            print(
                f"Warning: Invalid current weather data for {city}. "
                "Skipping record."
            )
            continue

        #  Check that all required fields exist
        required_fields = [
            "time",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]

        if any(field not in current for field in required_fields):
            print(
                f"Warning: Missing required weather fields for {city}. "
                "Skipping record."
            )
            continue

        #  Create a standardised weather record
        record = {
            "city": city,
            "timestamp": current["time"],
            "temperature_c": current["temperature_2m"],
            "humidity_percent": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"]
        }

        # Validate numeric values
        numeric_values = [
            record["temperature_c"],
            record["humidity_percent"],
            record["wind_speed_kmh"]
        ]

        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not pd.notna(value)
            for value in numeric_values
        ):
            print(
                f"Warning: Missing or invalid numeric value for {city}. "
                "Skipping record."
            )
            continue

        # Validate the timestamp
        timestamp = record["timestamp"]

        if (
            not isinstance(timestamp, str)
            or not timestamp.strip()
            or not pd.notna(timestamp)
        ):
            print(
                f"Warning: Missing or invalid timestamp for {city}. "
                "Skipping record."
            )
            continue

        #  Validate humidity
        if not 0 <= record["humidity_percent"] <= 100:
            print(
                f"Warning: Invalid humidity for {city}. "
                "Skipping record."
            )
            continue

        #  Validate temperature
        if not -90 <= record["temperature_c"] <= 60:
            print(
                f"Warning: Invalid temperature for {city}. "
                "Skipping record."
            )
            continue

        #  Validate wind speed
        if record["wind_speed_kmh"] < 0:
            print(
                f"Warning: Invalid wind speed for {city}. "
                "Skipping record."
            )
            continue

        # Add the valid record
        records.append(record)

    #  Convert records into a DataFrame
    dataframe = pd.DataFrame(
        records,
        columns=[
            "city",
            "timestamp",
            "temperature_c",
            "humidity_percent",
            "wind_speed_kmh"
        ]
    )

    # Remove duplicate city/timestamp combinations
    dataframe = dataframe.drop_duplicates(
        subset=["city", "timestamp"]
    )

    return dataframe.to_dict("records")


def save_processed_data(records):
    """
    Save the cleaned weather records to a CSV file.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(
        records,
        columns=[
            "city",
            "timestamp",
            "temperature_c",
            "humidity_percent",
            "wind_speed_kmh"
        ]
    )

    output_file = PROCESSED_DIR / "weather.csv"

    dataframe.to_csv(output_file, index=False)

    print(f"Saved processed data to: {output_file}")
    print(f"Total processed records: {len(dataframe)}")


def main():
    """
    Run the transformation stage.
    """
    records = transform_weather_data()
    save_processed_data(records)


if __name__ == "__main__":
    main()