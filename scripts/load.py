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

    dataframe.to_sql(
        "weather",
        connection,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(dataframe)} records into the database.")


def main():
    connection = create_database()

    try:
        load_weather_data(connection)
    finally:
        connection.close()

if __name__ == "__main__":
    main()