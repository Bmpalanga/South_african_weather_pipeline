from scripts.transform import transform_weather_data

def test_transform_weather_data():
    records = transform_weather_data()

    assert len(records) == 9