import sqlite3

from scripts.load import load_weather_data


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