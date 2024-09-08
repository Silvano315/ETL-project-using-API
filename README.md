# ETL-project-using-API

## Table of Contents
1. [Introduction](#introduction)
2. [Data Source](#data-source)
3. [Python Pipeline for Air Quality Monitoring](#python-pipeline-for-air-quality-monitoring)
   - [1. Data Extraction](#1-data-extraction)
   - [2. Data Cleaning](#2-data-cleaning)
   - [3. Data Transformation](#3-data-transformation)
   - [4. Data Loading](#4-data-loading)
   - [5. Data Visualization](#5-data-visualization)
   - [6. Automation and Scheduling](#6-automation-and-scheduling)
4. [Requirements](#requirements)


## Introduction

ETL stands for **Extract, Transform, Load**, which is a process used in data warehousing and analytics pipelines. It involves three main stages:

1. **Extract**: Collecting data from various sources, such as databases, APIs, or files.
2. **Transform**: Cleaning, normalizing, and transforming the extracted data to ensure consistency, quality, and relevance.
3. **Load**: Loading the transformed data into a data warehouse, database, or a data lake for further analysis and visualization.

The main advantages of the ETL Process could be:
- **Data Centralization**: ETL allows for consolidating data from various sources into a single, unified repository, making it easier to analyze and draw insights.
- **Data Quality**: By transforming and cleaning data, ETL processes help ensure that the data is consistent, accurate, and reliable.
- **Automation**: ETL pipelines can be scheduled to run at regular intervals, ensuring that the data is always up-to-date without manual intervention.

ETL processes are widely used in various fields, including: Business Intelligence (BI), Data Warehousing, Data Integration, Data Migration.

This project leverages the ETL process to monitor air quality in Milan using data extracted from an API available on [RapidAPI](https://rapidapi.com/weatherbit/api/air-quality). The ETL pipeline performs three main tasks:

1. **Extraction**: Air quality data is extracted from the RapidAPI's air-quality API using Python's `requests` library.
2. **Transformation**: The extracted data is then cleaned, formatted, and transformed to create additional features and remove any inconsistencies. This includes handling missing values, removing duplicates, converting data types, and generating new derived features.
3. **Loading**: The transformed data is saved in a CSV file and used to create various visualizations such as histograms, scatter plots, and time series, providing insights into the air quality in Milan.

The advantage of using this ETL approach is that it automates the entire data collection, transformation, and visualization process, allowing for continuous monitoring and analysis of air quality. The integration with the `schedule` library allows the pipeline to run at regular intervals (e.g., every 24 hours), ensuring the data is always fresh and up-to-date.


## Data from Rapid-API

The data utilized in this project was obtained from the Weatherbit Air Quality API, available through RapidAPI. This API allows users to access current air quality data, 3-day (hourly) air quality forecasts, and 24-hour historical air quality conditions for any location worldwide. For this project, the focus is on retrieving 24-hour historical air quality data for Milan, Italy.

The Weatherbit Air Quality API provides comprehensive information about air quality conditions, including both current and historical data. With this API, users can retrieve:

- **3-Day Hourly Forecasts**: Provides a forecast of air quality for the next 72 hours, broken down by the hour.
- **Current Air Quality + Pollen Levels**: Offers real-time data on air quality and pollen levels.
- **24-Hour Historical Data**: Supplies hourly historical air quality data for the past 24 hours for any location.

The dataset obtained from the API includes the following fields, which provide a detailed view of air quality conditions:

- **lat**: Latitude (Degrees) of the location.
- **lon**: Longitude (Degrees) of the location.
- **timezone**: Local IANA timezone for the location.
- **city_name**: Name of the nearest city.
- **country_code**: Country abbreviation.
- **state_code**: State abbreviation or code.
- **timestamp_local**: Local time of the measurement.
- **timestamp_utc**: Coordinated Universal Time (UTC) of the measurement.
- **ts**: Unix timestamp at UTC time.
- **aqi**: Air Quality Index (AQI) following the US EPA standard (ranges from 0 to 500).
- **o3**: Concentration of surface Ozone (O3) in micrograms per cubic meter (µg/m³).
- **so2**: Concentration of surface Sulfur Dioxide (SO2) in micrograms per cubic meter (µg/m³).
- **no2**: Concentration of surface Nitrogen Dioxide (NO2) in micrograms per cubic meter (µg/m³).
- **co**: Concentration of Carbon Monoxide (CO) in micrograms per cubic meter (µg/m³).
- **pm25**: Concentration of Particulate Matter (PM2.5) less than 2.5 micrometers in diameter (µg/m³).
- **pm10**: Concentration of Particulate Matter (PM10) less than 10 micrometers in diameter (µg/m³).

The data provided by the Weatherbit Air Quality API, accessed via RapidAPI, is sourced from reputable monitoring stations worldwide and updated regularly. This ensures high-quality, reliable data suitable for both real-time monitoring applications and long-term trend analysis.


## Python Pipeline for Air Quality Monitoring

The [`Python pipeline`](ETL_pipeline_air_quality.py) implemented in this project is designed to extract, transform, and load (ETL) data related to air quality monitoring in Milan, Italy. This pipeline uses Python to automate data processing and visualization tasks, providing valuable insights into air quality trends and pollution levels. The key components of the pipeline include:

### 1. Data Extraction

The extraction process utilizes the RapidAPI Air Quality API to retrieve historical air quality data for Milan.
The extraction step involves:
- Making HTTP requests to the RapidAPI endpoint.
- Handling the API response to ensure data integrity.
- Saving the raw data in JSON format for further processing.

### 2. Data Cleaning

Once the data is extracted, it undergoes a cleaning process to ensure its quality and usability. The cleaning steps include:
- Removing missing values and duplicates to prevent data inconsistencies.
- Converting timestamps to a uniform datetime format for proper time series analysis.
- Dropping unnecessary columns or those with only unique values to streamline the dataset.

### 3. Data Transformation

The transformation process involves reshaping and enriching the dataset to facilitate deeper insights. Key transformations include:
- Adding new columns derived from existing ones, such as pollutant ratios (e.g., PM10/PM2.5 ratio).
- Reformatting the DataFrame to include separate columns for year, month, day, and hour.
- Setting the `timestamp_local` as the index for time series analysis.

### 4. Data Loading

After the data is transformed, it is saved in a CSV format. This ensures that the cleaned and transformed data is stored in a structured format for future use or analysis. The loading step includes:
- Combining new transformed data with existing datasets to create a comprehensive and up-to-date record.
- Saving the updated data to a designated file location for easy access.

I also implemented a saving Data to SQLite Database:
- The transformed data is also appended to an existing `SQLite` database using `sqlite3` library. This allows for persistent storage and efficient querying of large datasets.
- The function is used to save the DataFrame (`df`) to the specified SQLite database [file](Data/air_quality.db). If the table already exists, new data is appended to it, ensuring that existing data is preserved and updated.

### 5. Data Visualization

To provide a more intuitive understanding of air quality trends and pollution levels, the pipeline includes a robust visualization component. Using the Plotly library, the following visualizations are generated and saved:
- **Histogram with Mean and Standard Deviation**: Visualizes the distribution of key air quality metrics.
- **Box Plot**: Displays the distribution and outliers of air quality data.
- **Correlation Matrix Heatmap**: Highlights relationships between different pollutants.
- **Time Series Plot**: Shows changes in air quality over time with an interactive range slider.
- **Scatter Plot with Regression Line**: Visualizes relationships between different pollutant concentrations.
- **Distribution Plot with KDE and Histogram**: Provides a dynamic, interactive view of the distributions of various pollutants.

These plots are saved in this [folder](Images/Air_Quality/) and they have the html format.

### 6. Automation and Scheduling

To keep the data up-to-date, the ETL pipeline is automated using the `schedule` library. The pipeline is set to run at regular intervals (e.g., every 24 hours) to fetch the latest air quality data and update the visualizations accordingly. This automation is implemented using Python's `threading` module to run the scheduler continuously in the background, allowing for uninterrupted data processing.


## Requirements

To run the Python pipeline, ensure that all the required libraries are installed. You can use the `requirements.txt` file generated by `pipreqs` to install them. To do this, run:

```bash
pip install -r requirements.txt
```

After that, to use the Python Pipeline:

1. **Configure API Keys**: Place your RapidAPI keys in the `API_keys.json` file in the correct format.
2. **Run the Pipeline**: Execute the ETL pipeline by running the Python script.
3. **Access Visualizations**: Visualizations will be saved in the `Images/Air_Quality/` directory for easy access and review.