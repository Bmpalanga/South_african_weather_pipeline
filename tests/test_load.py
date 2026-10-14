import sqlite3

from scripts.load import load_weather_data
from pathlib import Path
from unittest.mock import patch

import pytest
from unittest.mock import patch
from scripts.load import main
from scripts.load import create_database


def test_load_weather_data():
    connection = sqlite3.connect(":memory:")

    load_weather_data(connection)

    cursor = connection.execute(
        "SELECT COUNT(*) FROM weather"
    )

    count = cursor.fetchone()[0]

    assert count > 0

    connection.close()


def test_loading_data_twice_does_not_create_duplicates():
    connection = sqlite3.connect(":memory:")

    load_weather_data(connection)

    cursor = connection.execute(
        "SELECT COUNT(*) FROM weather"
    )

    first_count = cursor.fetchone()[0]

    load_weather_data(connection)

    cursor = connection.execute(
        "SELECT COUNT(*) FROM weather"
    )

    second_count = cursor.fetchone()[0]

    assert second_count == first_count

    connection.close()
    connection.close()
def test_loaded_weather_data_has_correct_values():
    connection = sqlite3.connect(":memory:")

    try:
        load_weather_data(connection)

        cursor = connection.execute("""
            SELECT city, timestamp, temperature_c,
                   humidity_percent, wind_speed_kmh
            FROM weather
            LIMIT 1
        """)

        row = cursor.fetchone()

        assert row is not None
        assert isinstance(row[0], str)
        assert isinstance(row[1], str)
        assert isinstance(row[2], (int, float))
        assert isinstance(row[3], (int, float))
        assert isinstance(row[4], (int, float))

    finally:
        connection.close()


def test_load_weather_data_raises_error_when_csv_is_missing():
    connection = sqlite3.connect(":memory:")

    missing_file = Path("data/processed/missing_weather.csv")

    try:
        with patch("scripts.load.CSV_FILE", missing_file):
            with pytest.raises(
                FileNotFoundError,
                match="Weather CSV file not found"
            ):
                load_weather_data(connection)

    finally:
        connection.close()     

def test_main_closes_connection_when_loading_fails():
    connection = sqlite3.connect(":memory:")

    with patch("scripts.load.create_database", return_value=connection):
        with patch(
            "scripts.load.load_weather_data",
            side_effect=FileNotFoundError("CSV file missing")
        ):
            with pytest.raises(FileNotFoundError):
                main()

    
    with pytest.raises(sqlite3.ProgrammingError):
        connection.execute("SELECT 1")
        
def test_create_database_creates_directory_and_database(tmp_path, monkeypatch):
    database_file = tmp_path / "new_database" / "weather.db"

    monkeypatch.setattr(
        "scripts.load.DATABASE_FILE",
        database_file
    )

    connection = create_database()

    try:
        assert database_file.parent.exists()
        assert database_file.exists()

        cursor = connection.execute("SELECT 1")
        assert cursor.fetchone()[0] == 1

    finally:
        connection.close()