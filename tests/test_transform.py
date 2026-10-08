from scripts.transform import transform_weather_data


def test_transform_weather_data():
    records = transform_weather_data()

    assert len(records) == 9


def test_transform_removes_duplicates():
    records = transform_weather_data()

    unique_records = {
        (record["city"], record["timestamp"])
        for record in records
    }

    assert len(unique_records) == len(records)