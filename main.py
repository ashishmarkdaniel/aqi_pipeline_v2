import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from supabase import create_client
# import json

def main():
    load_dotenv()
    WAQI_API_KEY = os.getenv("WAQI_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

    if not all([WAQI_API_KEY, SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY]):
        raise Exception("One or more environment variables are missing.")

    url = f"https://api.waqi.info/feed/@10111/?token={WAQI_API_KEY}"

    try:
        api_response = requests.get(url, timeout=30)
        api_response.raise_for_status()
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

    data = api_response.json()
    if data["status"] != "ok":
        raise Exception(f"WAQI API Error: {data}")

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY
    )

    # with open("sample_response.json", "r") as f:
    #     data = json.load(f)

    ingest_ts = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()

    measurement_time = data["data"]["time"]["iso"]

    data_provider_entity = data["data"]["attributions"][0]["name"]

    city_name = data["data"]["city"]["name"]

    aqi = data["data"]["aqi"]

    dominant_pollutant = data["data"]["dominentpol"]

    #iaqi contains pollutant list with corresponding value.
    pollutant_all_dict = data["data"]["iaqi"]

    rows = []
    #1. All pollutants table
    for pollutant, value_dict in pollutant_all_dict.items():

        row = {
            "ingest_ts" : ingest_ts,
            "measurement_time" : measurement_time,
            "data_provider_entity" : data_provider_entity,
            "city_name" : city_name,
            "dominant_pollutant" : dominant_pollutant,
            "aqi" : aqi,
            "pollutant" : pollutant,
            "pollutant_value" : value_dict["v"]
        }

        rows.append(row)

    insert_aqi_all_pollutant_daily = (
        supabase
        .table("aqi_all_pollutant_daily")
        .insert(rows)
        .execute()
    )

    print(f"aqi_all_pollutant_daily: Inserted {len(rows)} current pollutant rows.")
    print(f"Database response: {insert_aqi_all_pollutant_daily.data}")

    #2 D-1 summary table

    measurement_date = datetime.fromisoformat(measurement_time)

    yesterday = (measurement_date - timedelta(days=1)).strftime("%Y-%m-%d")

    daily_pollutant_list = ["pm10", "pm25", "uvi"]

    daily_rows = []

    for pollutant in daily_pollutant_list:
        pollutant_data = data["data"]["forecast"]["daily"].get(pollutant, [])
        # print(pollutant_data)
        for measured_val in pollutant_data:
            if measured_val["day"] == yesterday:
                row = {
                    "ingest_ts" : ingest_ts,
                    "measurement_date" : measured_val["day"],
                    "min_of_day" : measured_val["min"],
                    "max_of_day" : measured_val["max"],
                    "avg_of_day" : measured_val["avg"],
                    "pollutant" : pollutant
                }
                daily_rows.append(row)
                break

    insert_aqi_summary_daily = (
        supabase
        .table("aqi_summary_daily")
        .insert(daily_rows)
        .execute()
    )

    print(f"aqi_summary_daily: Inserted {len(daily_rows)} summary rows.")
    print(f"Database response: {insert_aqi_summary_daily.data}")

if __name__ == "__main__":
    main()