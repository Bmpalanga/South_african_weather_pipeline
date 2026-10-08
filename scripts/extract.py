import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": -33.9249,
    "longitude": 18.4241,
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m"
    ]
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.json())