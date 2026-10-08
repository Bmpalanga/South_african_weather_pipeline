import sqlite3

from scripts.load import load_weather_data


def test_load_weather_data():
    connection = sqlite3.connect(":memory:")

    load_weather_data(connection)

    cursor = connection.execute(
        "SELECT COUNT(*) FROM weather"
    )

    count = cursor.fetchone()[0]

    assert count == 9

    connection.close()