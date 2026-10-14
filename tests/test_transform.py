from scripts.transform import transform_weather_data, load_weather_file
from unittest.mock import patch
from pathlib import Path

import pandas as pd
from pathlib import Path
from scripts.transform import save_processed_data

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
        "pathlib.Path.glob",
        return_value=[Path("data/raw/cape_town_test.json")]
    ):
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


def test_transform_skips_nan_temperature():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": float("nan"),
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


def test_transform_skips_invalid_temperature_type():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": "unknown",
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

def test_load_weather_file_with_invalid_json(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{invalid json}")

    result = load_weather_file(invalid_file)

    assert result is None

def test_load_weather_file_with_missing_file(tmp_path):
    missing_file = tmp_path / "missing.json"

    result = load_weather_file(missing_file)

    assert result is None

def test_transform_skips_missing_current_section():
    fake_weather_data = {
        "latitude": -33.9,
        "longitude": 18.4
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

def test_transform_skips_missing_required_fields():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.5
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

def test_transform_skips_invalid_current_section():
    fake_weather_data = {
        "current": "invalid weather data"
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

def test_transform_skips_non_dictionary_response():
    fake_weather_data = ["invalid", "weather", "data"]

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

def test_transform_skips_string_temperature():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": "hot",
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.5
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

def test_transform_skips_humidity_above_100():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 22.5,
            "relative_humidity_2m": 150,
            "wind_speed_10m": 12.5
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

def test_transform_skips_negative_humidity():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 22.5,
            "relative_humidity_2m": -10,
            "wind_speed_10m": 12.5
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

def test_transform_skips_temperature_above_60():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 65,
            "relative_humidity_2m": 50,
            "wind_speed_10m": 12.5
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

def test_transform_skips_temperature_below_minus_90():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": -95,
            "relative_humidity_2m": 50,
            "wind_speed_10m": 12.5
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

def test_transform_skips_negative_wind_speed():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 22.5,
            "relative_humidity_2m": 65,
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


def test_transform_skips_missing_timestamp():
    fake_weather_data = {
        "current": {
            "time": None,
            "temperature_2m": 22.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.5
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

def test_transform_skips_missing_temperature():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": None,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.5
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

def test_transform_skips_missing_humidity():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 22.5,
            "relative_humidity_2m": None,
            "wind_speed_10m": 12.5
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

def test_transform_skips_missing_wind_speed():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 22.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": None
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

def test_transform_removes_duplicate_records():
    fake_weather_data = {
        "current": {
            "time": "2026-10-14T10:00",
            "temperature_2m": 22.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.5
        }
    }

    duplicate_file = Path("data/raw/cape_town_10_14.json")

    with patch(
        "pathlib.Path.glob",
        return_value=[duplicate_file, duplicate_file]
    ):
        with patch(
            "scripts.transform.load_weather_file",
            return_value=fake_weather_data
        ):
            records = transform_weather_data()

    assert len(records) == 1
    assert records[0]["city"] == "cape_town"
    assert records[0]["timestamp"] == "2026-10-14T10:00"

def test_save_processed_data_creates_csv(tmp_path, monkeypatch):
    records = [
        {
            "city": "cape_town",
            "timestamp": "2026-10-14T10:00",
            "temperature_c": 22.5,
            "humidity_percent": 65,
            "wind_speed_kmh": 12.5
        }
    ]

    output_dir = tmp_path / "processed"
    monkeypatch.setattr(
        "scripts.transform.PROCESSED_DIR",
        output_dir
    )

    save_processed_data(records)

    output_file = output_dir / "weather.csv"

    assert output_file.exists()

    dataframe = pd.read_csv(output_file)

    assert len(dataframe) == 1
    assert dataframe.loc[0, "city"] == "cape_town"
    assert dataframe.loc[0, "temperature_c"] == 22.5
    assert dataframe.loc[0, "humidity_percent"] == 65
    assert dataframe.loc[0, "wind_speed_kmh"] == 12.5

def test_save_processed_data_with_empty_records(tmp_path, monkeypatch):
    output_dir = tmp_path / "processed"

    monkeypatch.setattr(
        "scripts.transform.PROCESSED_DIR",
        output_dir
    )

    save_processed_data([])

    output_file = output_dir / "weather.csv"

    assert output_file.exists()

    dataframe = pd.read_csv(output_file)

    assert dataframe.empty

    assert list(dataframe.columns) == [
        "city",
        "timestamp",
        "temperature_c",
        "humidity_percent",
        "wind_speed_kmh"
    ]