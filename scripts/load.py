import sqlite3
import pandas as pd
from pathlib import Path

CSV_FILE = Path("data/processed/weather.csv")
DATABASE_FILE = Path("database/weather.db")


def create_database():
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)
    return connection


def load_weather_data(connection):
    dataframe = pd.read_csv(CSV_FILE)

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

    connection.commit()

    print(f"Processed {len(dataframe)} records.")


def main():
    connection = create_database()

    try:
        load_weather_data(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()