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