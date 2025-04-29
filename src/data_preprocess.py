import pandas as pd
import numpy as np

# =====================================================
# 1. Configuration
# =====================================================
INPUT_PATHS = {
    "diabetes": "../data/raw/cdc_diabetes.csv",
    "census": "../data/raw/census_socioeconomic.csv",
    "food_access": "../data/raw/usda_food_access.csv",
    "rural_urban": "../data/raw/rural_urban_codes.csv"
}

OUTPUT_PATH = "../data/processed/final_dataset.csv"

# =====================================================
# 2. Helper Functions
# =====================================================

def normalize_name(name: str) -> str:
    """Normalize geographic names for consistent merging"""
    return (
        str(name).lower()
        .replace("county", "")
        .replace(",", "")
        .strip()
    )

def extract_geo_components(location: str) -> tuple:
    """Extract county and state from location strings"""
    parts = str(location).split(",")
    return (
        normalize_name(parts[0]),
        normalize_name(parts[1]) if len(parts) > 1 else ""
    )

# =====================================================
# 3. Data Cleaning Components
# =====================================================

def process_food_access() -> pd.DataFrame:
    """Clean and aggregate USDA food access data"""
    df = pd.read_csv(INPUT_PATHS["food_access"])
    
    # Validate required columns
    req_cols = ["State", "County", "LA1and10", "LILATracts_1And10"]
    if not set(req_cols).issubset(df.columns):
        raise ValueError("Missing required columns in food access data")
    
    return (
        df[req_cols]
        .groupby(["State", "County"])
        .agg({"LA1and10": "sum", "LILATracts_1And10": "sum"})
        .reset_index()
        .rename(columns={"State": "state", "County": "county"})
    )

def process_rural_urban() -> pd.DataFrame:
    """Process rural-urban classification data"""
    df = pd.read_csv(INPUT_PATHS["rural_urban"], encoding='latin-1')
    
    # Clean and transform
    return (
        df[["FIPS", "Value"]]
        .rename(columns={"Value": "RuralUrbanCode"})
        .assign(
            RuralUrbanCode=lambda x: pd.to_numeric(x.RuralUrbanCode, errors="coerce"),
            is_rural=lambda x: np.where(x.RuralUrbanCode >= 4, 1, 0)
        )
        [["FIPS", "is_rural"]]
    )

def process_diabetes() -> pd.DataFrame:
    """Clean and validate diabetes data"""
    df = pd.read_csv(INPUT_PATHS["diabetes"])
    
    return (
        df.assign(
            state_only=df["locationdesc"].apply(lambda x: normalize_name(x))
        )
        .groupby("state_only")
        .agg({
            "yearstart": "first",
            "datavaluetype": "first",
            "datavalue": "first"
        })
        .reset_index()
        .rename(columns={"datavalue": "diabetes_prevalence"})
        .pipe(lambda df: df[
            (df.diabetes_prevalence.between(5, 20)) &
            (df.datavaluetype == "Crude Prevalence")
        ])
    )

def process_census() -> pd.DataFrame:
    """Process census socioeconomic data"""
    df = pd.read_csv(INPUT_PATHS["census"])
    
    # Extract geographic components
    geo_components = df["county_name"].apply(
        lambda x: pd.Series(extract_geo_components(x), 
                          index=["county_clean", "state_clean"])
    )
    
    return pd.concat([df, geo_components], axis=1).assign(
        state=lambda x: x.state_clean.str.title(),
        county=lambda x: x.county_clean.str.title(),
        state_only=lambda x: x.state_clean
    )

# =====================================================
# 4. Core Processing Pipeline
# =====================================================

def merge_datasets() -> pd.DataFrame:
    """Main data merging pipeline"""
    # Process individual datasets
    census_df = process_census()
    diabetes_df = process_diabetes()
    food_df = process_food_access()
    rural_df = process_rural_urban()

    # Merge sequence
    merged = (
        census_df
        .merge(diabetes_df, on="state_only", how="inner")
        .merge(food_df, on=["state", "county"], how="left")
        .merge(rural_df, on="FIPS", how="left")
    )
    
    return merged

def finalize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Apply final transformations and validations"""
    return (
        df
        .rename(columns={"yearstart": "year"})
        [[
            "state", "county", "year", "diabetes_prevalence",
            "poverty_population", "FIPS", "LA1and10", 
            "LILATracts_1And10", "is_rural"
        ]]
        .assign(
            diabetes_prevalence=lambda x: x.diabetes_prevalence.clip(5, 20),
            is_rural=lambda x: x.is_rural.fillna(0).astype(int),
            FIPS=lambda x: x.FIPS.astype(str).str.zfill(5)
        )
        .drop_duplicates()
        .sort_values(["state", "county"])
    )

# =====================================================
# 5. Main Execution
# =====================================================

def preprocess_data():
    """Orchestrate full preprocessing workflow"""
    try:
        final_df = finalize_dataset(merge_datasets())
        final_df.to_csv(OUTPUT_PATH, index=False)
        
        print("Successfully processed data:")
        print(f"- Total counties: {len(final_df)}")
        print(f"- Diabetes range: {final_df.diabetes_prevalence.min()}%-{final_df.diabetes_prevalence.max()}%")
        print(f"- Rural counties: {final_df.is_rural.sum()} ({final_df.is_rural.mean():.1%})")
        
        return final_df
        
    except Exception as e:
        print(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    preprocess_data()