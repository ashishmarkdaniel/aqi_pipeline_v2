# AQI ETL Pipeline

An end-to-end data engineering project that extracts Air Quality Index (AQI) data from the World Air Quality Index (WAQI) API, transforms it into analytics-ready datasets, loads it into a PostgreSQL database hosted on Supabase, and automates the entire pipeline using GitHub Actions.

## Project Overview

This project demonstrates a production-style ETL pipeline using Python and cloud services.

The pipeline runs automatically every day, collects the latest AQI measurements for a monitoring station, stores both current pollutant readings and historical daily summaries in PostgreSQL, and serves as the data source for a Power BI dashboard.

## Architecture

```text
                 WAQI API
                     │
                     ▼
             Python ETL Script
                     │
                     ▼
           GitHub Actions (Daily)
                     │
                     ▼
         Supabase PostgreSQL Database
                     │
                     ▼
              Power BI Dashboard
```

## Tech Stack

- Python
- Requests
- Supabase Python SDK
- PostgreSQL (Supabase)
- GitHub Actions
- Power BI
- World Air Quality Index (WAQI) API

## ETL Workflow

### Extract

- Fetches real-time AQI data from the WAQI API.
- Validates both HTTP response status and WAQI API status.
- Handles request failures with exception handling and timeouts.

### Transform

Creates two datasets:

#### 1. Current Pollutant Measurements

Stores the latest values for all available pollutants, including:

- AQI
- Dominant Pollutant
- PM2.5
- PM10
- UVI
- Additional pollutants when available

#### 2. Previous Day Summary

Extracts the previous day's forecast summary for:

- PM2.5
- PM10
- UVI

including:

- Minimum value
- Maximum value
- Average value

### Load

Bulk inserts transformed data into two PostgreSQL tables hosted on Supabase:

- `aqi_all_pollutant_daily`
- `aqi_summary_daily`

## Features

- Automated daily ETL using GitHub Actions
- Secure secret management using GitHub Secrets
- Environment variable validation
- API timeout and exception handling
- Bulk database inserts
- Logging of ETL execution
- Timezone-aware timestamps (Asia/Kolkata)

## Database Schema

### aqi_all_pollutant_daily

| Column |
|---------|
| ingest_ts |
| measurement_time |
| city_name |
| data_provider_entity |
| dominant_pollutant |
| aqi |
| pollutant |
| pollutant_value |

### aqi_summary_daily

| Column |
|---------|
| ingest_ts |
| measurement_date |
| pollutant |
| min_of_day |
| max_of_day |
| avg_of_day |

## Automation

The pipeline runs automatically every day using GitHub Actions.

It can also be triggered manually using the **workflow_dispatch** event for testing.

## Future Improvements

- Support multiple monitoring stations
- Historical backfill

## Learning Outcomes

This project demonstrates experience with:

- ETL design
- Data transformation
- PostgreSQL
- Cloud-hosted databases
- GitHub Actions
- Environment variable management
- Python automation
- Power BI integration
