import sqlite3
import pandas as pd
from pathlib import Path


# Input CSV file containing processed weather data
CSV_FILE = Path("data/processed/weather.csv")

# SQLite database location
DATABASE_FILE = Path("database/weather.db")


def create_database():
    """
    Create the database directory if necessary
    and establish a database connection.
    """
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    return connection


def load_weather_data(connection):
    """
    Load processed weather data from CSV into SQLite.

    Raises:
        FileNotFoundError: If the processed CSV file does not exist.
    """
    # Read the processed CSV file
    try:
        dataframe = pd.read_csv(CSV_FILE)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Weather CSV file not found: {CSV_FILE}"
        ) from error

    # Create the weather table if it does not exist
    connection.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            temperature_c REAL,
            humidity_percent REAL,
            wind_speed_kmh REAL,
            UNIQUE(city, timestamp)
        )
    """)

    # Insert weather records and ignore duplicates
    for _, row in dataframe.iterrows():
        connection.execute("""
            INSERT OR IGNORE INTO weather (
                city,
                timestamp,
                temperature_c,
                humidity_percent,
                wind_speed_kmh
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            row["city"],
            row["timestamp"],
            row["temperature_c"],
            row["humidity_percent"],
            row["wind_speed_kmh"]
        ))

    # Save changes to the database
    connection.commit()

    print(f"Processed {len(dataframe)} records.")


def main():
    """
    Run the database loading process and close the connection.
    """
    connection = create_database()

    try:
        load_weather_data(connection)

    finally:
        connection.close()


if __name__ == "__main__":
    main()