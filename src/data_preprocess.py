import pandas as pd

# =====================================================
# 1. Food Access Data Cleaning
# =====================================================
def clean_food_access_data():
    food_df = pd.read_csv("../data/raw/usda_food_access.csv")
    
    # Keep essential columns
    food_clean = food_df[["State", "County", "LA1and10", "LILATracts_1And10"]]
    
    # Aggregate to county level
    return food_clean.groupby(["State", "County"]).agg({
        "LA1and10": "sum",
        "LILATracts_1And10": "sum"
    }).reset_index()

# =====================================================
# 2. Rural-Urban Data Cleaning
# =====================================================
def clean_rural_urban_data():
    rural_df = pd.read_csv("../data/raw/rural_urban_codes.csv", encoding='latin-1')
    
    # Process rural-urban codes
    rural_clean = rural_df[["FIPS", "Value"]].copy()
    rural_clean.rename(columns={"Value": "RuralUrbanCode"}, inplace=True)
    
    rural_clean["RuralUrbanCode"] = pd.to_numeric(
        rural_clean["RuralUrbanCode"], errors="coerce"
    )
    rural_clean["is_rural"] = rural_clean["RuralUrbanCode"].apply(
        lambda x: 1 if x >= 4 else 0
    )
    
    return rural_clean[["FIPS", "is_rural"]]

# =====================================================
# 3. Helper Functions
# =====================================================
def normalize_name(name):
    return (
        str(name).lower()
        .replace("county", "")
        .replace(",", "")
        .strip()
        if pd.notnull(name) else ""
    )

def extract_county_and_state(location):
    if pd.isna(location):
        return "", ""
    parts = str(location).split(",")
    return (
        normalize_name(parts[0]),
        normalize_name(parts[1]) if len(parts) > 1 
        else (normalize_name(location), "")
    )

def extract_state(location):
    return normalize_name(location) if pd.notnull(location) else ""

# =====================================================
# 4. Main Preprocessing Pipeline
# =====================================================
def preprocess_data():
    # Load core datasets
    diabetes_df = pd.read_csv("../data/raw/cdc_diabetes.csv")
    census_df = pd.read_csv("../data/raw/census_socioeconomic.csv")
    
    # Process supplementary data
    food_df = clean_food_access_data()
    rural_df = clean_rural_urban_data()

    # =====================
    # Census Data Processing
    # =====================
    census_df[['county_clean', 'state_clean']] = census_df['county_name'].apply(
        lambda x: pd.Series(extract_county_and_state(x))
    )
    census_df = census_df.assign(
        state=census_df['state_clean'].str.title(),
        county=census_df['county_clean'].str.title(),
        state_only=census_df['state_clean']
    )

    # ======================
    # Diabetes Data Processing
    # ======================
    diabetes_state = diabetes_df.assign(
        state_only=diabetes_df['locationdesc'].apply(extract_state)
    ).groupby("state_only").agg({
        "yearstart": "first",
        "datavaluetype": "first",
        "datavalue": "first"
    }).reset_index()

    # ==============
    # Merge Sequence
    # ==============
    merged = (
        pd.merge(census_df, diabetes_state, on="state_only", how="inner")
        .merge(food_df.rename(columns={
            "State": "state",
            "County": "county"
        }), on=["state", "county"], how="left")
        .merge(rural_df, on="FIPS", how="left")
    )

    # ================
    # Finalize Dataset
    # ================
    final_df = merged[[
        "state", "county", "yearstart", "datavaluetype",
        "datavalue", "poverty_population", "FIPS",
        "LA1and10", "LILATracts_1And10", "is_rural"
    ]].rename(columns={
        "yearstart": "year",
        "datavaluetype": "metric_type",
        "datavalue": "diabetes_prevalence"
    })

    # Type conversions
    final_df = final_df.assign(
        diabetes_prevalence=pd.to_numeric(
            final_df["diabetes_prevalence"], errors="coerce"
        ),
        year=final_df["year"].astype(int)
    ).dropna(subset=["diabetes_prevalence"])

    # Save processed data
    final_df.to_csv("../data/processed/final_dataset.csv", index=False)
    print("Processed data saved to data/processed/final_dataset.csv")
    return True

if __name__ == "__main__":
    preprocess_data()