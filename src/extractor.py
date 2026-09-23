import os
import json
import requests
import pandas as pd
from datetime import datetime
import gspread

def fetch_metmalaysia_forecast():
    print("Fetching live climate data for Perasaan Malaysia...")
    
    url = "https://api.data.gov.my/weather/forecast"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

    if not data:
        print("API returned no data.")
        return None

    forecast_list = []
    
    for item in data:
        loc_data = item.get("location", {})
        location_id = str(loc_data.get("location_id", ""))
        location_name = loc_data.get("location_name", "Unknown")
        
        if location_id.startswith("St"):
            loc_type_str = "State"
        elif location_id.startswith("Ds"):
            loc_type_str = "District"
        else:
            continue

        forecast_list.append({
            "Extraction_Date": datetime.now().strftime("%Y-%m-%d"),
            "Location_ID": location_id,
            "Location_Name": location_name,
            "Location_Type": loc_type_str,
            "Forecast_Date": item.get("date"),
            "Morning_Forecast": item.get("morning_forecast"),
            "Afternoon_Forecast": item.get("afternoon_forecast"),
            "Night_Forecast": item.get("night_forecast"),
            "Summary_Forecast": item.get("summary_forecast"),
            "Min_Temp_C": item.get("min_temp"),
            "Max_Temp_C": item.get("max_temp")
        })

    df = pd.DataFrame(forecast_list)
    return df

def push_to_google_sheets(df):
    print("Authenticating and pushing data to Google Sheets...")
    
    # Check if credentials exist in environment (for GitHub Actions) or local file
    sa_env = os.environ.get("GCP_SA_KEY")
    if sa_env:
        service_account_info = json.loads(sa_env)
        gc = gspread.service_account_from_dict(service_account_info)
    else:
        gc = gspread.service_account(filename="credentials.json")
    
    sh = gc.open("Perasaan Malaysia")
    worksheet = sh.sheet1
    
    df = df.fillna("")
    data_to_write = [df.columns.values.tolist()] + df.values.tolist()
    
    worksheet.clear()
    worksheet.update(values=data_to_write, range_name="A1")
    
    print("Database sync complete.")

if __name__ == "__main__":
    df_climate = fetch_metmalaysia_forecast()
    
    if df_climate is not None and not df_climate.empty:
        print(f"Successfully extracted {len(df_climate)} forecast records.")
        push_to_google_sheets(df_climate)
    else:
        print("No data was processed.")