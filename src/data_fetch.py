import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from census import Census

load_dotenv()

# CDC API Configuration
CDC_URL = "https://data.cdc.gov/resource/hksd-2xuw.json"
CDC_PARAMS = {
    "$$app_token": os.getenv("CDC_APP_TOKEN"),
    "$where": "topic == 'Diabetes'",  # Filter diabetes-related indicators
    "$limit": 50000
}

# Census Configuration
CENSUS_KEY = os.getenv("CENSUS_API_KEY")
c = Census(CENSUS_KEY)

def fetch_cdc_data():
    print("Fetching CDC diabetes data...")
    offset = 0
    all_data = []
    
    while True:
        try:
            params = {**CDC_PARAMS, "$offset": offset}
            response = requests.get(CDC_URL, params=params)
            response.raise_for_status()
            
            chunk = response.json()
            if not chunk:
                break
                
            all_data.extend(chunk)
            offset += CDC_PARAMS["$limit"]
            print(f"Fetched {len(chunk)} rows (total: {len(all_data)})")
            time.sleep(1)  # Avoid rate limits
            
        except Exception as e:
            print(f"Error: {e}")
            break

    df = pd.DataFrame(all_data)
    df.to_csv("../data/raw/cdc_diabetes.csv", index=False)
    print("CDC data saved to data/raw/cdc_diabetes.csv")

def fetch_census_data():
    print("Fetching Census socioeconomic data...")
    
    # Use the same parameters as your browser test
    variables = ["NAME", "B17001_001E"]  # Poverty rate variable
    year = 2019  # Must match the year you tested in the browser
    
    # Fetch data for all counties in all states
    census_data = c.acs5.get(
        variables,
        {"for": "county:*", "in": "state:*"},
        year=year
    )
    
    # Convert to DataFrame
    df = pd.DataFrame(census_data)
    
    # Clean and format
    df.columns = ["county_name", "poverty_population", "state_fips", "county_fips"]
    df["FIPS"] = df["state_fips"] + df["county_fips"]
    
    df.to_csv("../data/raw/census_socioeconomic.csv", index=False)
    print("Census data saved to data/raw/census_socioeconomic.csv")

if __name__ == "__main__":
    fetch_cdc_data()
    fetch_census_data()