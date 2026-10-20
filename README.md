# South African Weather Pipeline

## 1. Project Overview

This project is a Python data engineering pipeline that collects weather data for nine cities in South Africa using the Open-Meteo API.

The pipeline follows the Extract, Transform, Load (ETL) process. It collects weather observations, transforms the data into a structured format, stores the results in an SQLite database, and analyses weather conditions across the selected cities.

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
 


## 5. Installation and Setup

### Create a virtual environment

```bash
python3 -m venv .venv

# Install project dependencies
python -m pip install -r requirements.txt

# Run the weather pipeline
python run_pipeline.py

# Start the Jupyter pipeline
jupyter notebook

# If the browser does not open automatically ,use:
jupyter notebook --no-browser

# Run automated tests
python -m pytest

```
## 6. Data storage

The project uses the following storage formats:
> JSON: raw API responses
> CSV  : Processed weather observations
> SQLITE : Structured weather data stored in a database

### Project structure
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
├── scripts/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   ├── test_load.py
│   ├── test_pipeline.py
│   └── test_transform.py
├── run_pipeline.py
├── requirements.txt
├── pytest.ini
└── README.md

## Project Tracking
WeThinkCode activity ID : WTC-ENMDPD4G