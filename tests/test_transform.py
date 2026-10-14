from scripts.transform import transform_weather_data
from unittest.mock import patch
from pathlib import Path


def test_transform_weather_data():
    records = transform_weather_data()

    assert len(records) > 0

    for record in records:
        assert "city" in record
        assert "timestamp" in record
        assert "temperature_c" in record
        assert "humidity_percent" in record
        assert "wind_speed_kmh" in record


def test_transform_removes_duplicates():
    records = transform_weather_data()

    unique_records = {
        (record["city"], record["timestamp"])
        for record in records
    }

    assert len(unique_records) == len(records)

    from scripts.transform import transform_weather_data


def test_transform_weather_data():
    records = transform_weather_data()

    assert len(records) > 0

    for record in records:
        assert "city" in record
        assert "timestamp" in record
        assert "temperature_c" in record
        assert "humidity_percent" in record
        assert "wind_speed_kmh" in record


def test_transform_removes_duplicates():
    records = transform_weather_data()

    unique_records = {
        (record["city"], record["timestamp"])
        for record in records
    }

    assert len(unique_records) == len(records)

def test_humidity_must_be_between_0_and_100():
    valid_humidity_values = [0, 45, 100]
    invalid_humidity_values = [-1, 101]

    for humidity in valid_humidity_values:
        assert 0 <= humidity <= 100

    for humidity in invalid_humidity_values:
        assert not 0 <= humidity <= 100


def test_temperature_must_be_within_valid_range():
    valid_temperatures = [-90, 20, 60]
    invalid_temperatures = [-91, 61]

    for temperature in valid_temperatures:
        assert -90 <= temperature <= 60

    for temperature in invalid_temperatures:
        assert not -90 <= temperature <= 60

def test_wind_speed_must_not_be_negative():
    valid_wind_speeds = [0, 10, 20.5]
    invalid_wind_speeds = [-1, -5]

    for wind_speed in valid_wind_speeds:
        assert wind_speed >= 0

    for wind_speed in invalid_wind_speeds:
        assert not wind_speed >= 0

def test_weather_record_has_no_missing_values():
    valid_record = {
        "city": "cape_town",
        "timestamp": "2026-10-14T10:00",
        "temperature_c": 20.5,
        "humidity_percent": 65,
        "wind_speed_kmh": 12.0
    }

    assert all(value is not None for value in valid_record.values())

def test_transform_skips_invalid_humidity():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 20.5,
            "relative_humidity_2m": 120,
            "wind_speed_10m": 12.0
        }
    }

    with patch(
    "scripts.transform.RAW_DIR",
    new=Path("data/raw")
):
     with patch(
        "pathlib.Path.glob",
        return_value=[Path("data/raw/cape_town_test.json")]
    ):
        with patch(
            "scripts.transform.load_weather_file",
            return_value=fake_weather_data
        ):
            records = transform_weather_data()
        
        with patch(
            "scripts.transform.load_weather_file",
            return_value=fake_weather_data
        ):
            records = transform_weather_data()

    assert records == []

def test_transform_skips_invalid_temperature():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 70,
            "relative_humidity_2m": 50,
            "wind_speed_10m": 12.0
        }
    }

    with patch(
        "pathlib.Path.glob",
        return_value=[Path("data/raw/cape_town_test.json")]
    ):
        with patch(
            "scripts.transform.load_weather_file",
            return_value=fake_weather_data
        ):
            records = transform_weather_data()

    assert records == []

def test_transform_skips_invalid_wind_speed():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 20.5,
            "relative_humidity_2m": 50,
            "wind_speed_10m": -5
        }
    }

    with patch(
        "pathlib.Path.glob",
        return_value=[Path("data/raw/cape_town_test.json")]
    ):
        with patch(
            "scripts.transform.load_weather_file",
            return_value=fake_weather_data
        ):
            records = transform_weather_data()

    assert records == []

def test_transform_skips_missing_values():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": None,
            "relative_humidity_2m": 50,
            "wind_speed_10m": 12.0
        }
    }

    with patch(
        "pathlib.Path.glob",
        return_value=[Path("data/raw/cape_town_test.json")]
    ):
        with patch(
            "scripts.transform.load_weather_file",
            return_value=fake_weather_data
        ):
            records = transform_weather_data()

    assert records == []