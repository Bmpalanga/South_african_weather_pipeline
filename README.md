# South_african_weather_pipeline

## 1. Project Overview

This project is a Python data engineering pipeline that collects
weather data for nine cities in South Africa using the Open-Meteo API.

The pipeline follows the Extract, Transform, Load (ETL) process.

It collects weather observations, transforms the data into a
structured format, stores the results in an SQLite database,
and analyses weather conditions across the selected cities.

## 2. Project Objectives

- Collect weather data from an external API.
- Extract data for nine South African cities.
- Transform raw JSON data into structured tabular data.
- Remove duplicate city and timestamp records.
- Store weather observations in an SQLite database.
- Analyse temperature, humidity, and wind speed.
- Visualise weather comparisons using Python.

## 3. Technologies Used

- Python 3.12
- Open-Meteo API
- Requests
- Pandas
- Matplotlib
- SQLite
- Jupyter Notebook
- Pytest
- Git and GitHub

## 4. Cities Covered

The pipeline collects weather observations for:

1. Cape Town
2. Johannesburg
3. Durban
4. Pretoria
5. Bloemfontein
6. Gqeberha
7. East London
8. Polokwane
9. Mbombela

## Installation and setup

# Creating virtual enevironment
-python3 -m venv .venv

# activatin environment on Linux
-source .venv/bin/activate

# installing project dependencies
-python -m pip install -r requirements.txt

# running pipeline
-python run_pipeline.py

# running tests
-python -m pytest

## Data Storage
1. JSON for raw API responses
2. CSV for processed weather observations
3. SQLite for structured database storage


## 5. Project Structure


South_african_weather_pipeline/
├── config/
│   └── config.json
├── data/
│   ├── raw/
│   └── processed/
│       └── weather.csv
├── database/
│   └── weather.db
├── notebooks/
│   └── weather_analysis.ipynb
├── scripts/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   ├── test_load.py
│   └── test_transform.py
├── run_pipeline.py
├── requirements.txt
├── pytest.ini
└── README.md