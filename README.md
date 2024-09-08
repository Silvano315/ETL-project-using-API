# ETL-project-using-API

## Table of Contents
1. [Introduction](#introduction)
2. [Data from Rapid-Api](#data-from-rapid-api)
3. [Python Pipeline for Air Quality Monitoring](#python-pipeline-air-quality-monitoring)
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

## Data from Rapid API


## Python Pipeline for Air Quality Monitoring


## Requirements
