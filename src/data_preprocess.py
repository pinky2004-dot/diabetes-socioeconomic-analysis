import pandas as pd

def normalize_name(name):
    """Normalize names for consistent merging"""
    if isinstance(name, str):
        return name.lower().replace('county', '').replace(',', '').strip()
    return ""

def extract_state(text):
    """Extract state from location strings"""
    if not isinstance(text, str):
        return ""
    if ',' in text:
        return normalize_name(text.split(',')[1])
    return normalize_name(text)

def preprocess_data():
    print("Loading CDC diabetes data and Census Socioeconomics data...")
    # Load raw data
    diabetes_df = pd.read_csv("../data/raw/cdc_diabetes.csv")
    census_df = pd.read_csv("../data/raw/census_socioeconomic.csv")

    print("Processing CDC diabetes data...")
    # Process diabetes data
    diabetes_df['state_only'] = diabetes_df['locationdesc'].apply(extract_state)
    diabetes_state = diabetes_df.groupby('state_only').agg({
        'yearstart': 'first',
        'datavaluetype': 'first',
        'datavalue': 'first'
    }).reset_index()

    print("Processing census socioeconomics data...")
    # Process census data
    census_df['state_only'] = census_df['county_name'].apply(extract_state)

    print("Merging CDC diabetes data and census socioeconomics data...")
    # Merge datasets
    merged_df = pd.merge(
        census_df,
        diabetes_state,
        on='state_only',
        how='inner'
    )

    # Format final output
    final_df = merged_df[[
        'state_only', 'county_name', 'yearstart',
        'datavaluetype', 'datavalue', 'poverty_population', 'FIPS'
    ]].copy()

    final_df.rename(columns={
        'state_only': 'state',
        'county_name': 'county',
        'yearstart': 'year',
        'datavaluetype': 'metric_type',
        'datavalue': 'diabetes_prevalence'
    }, inplace=True)

    # Clean and type conversion
    final_df['state'] = final_df['state'].str.title()
    final_df['county'] = final_df['county'].str.title()
    final_df['diabetes_prevalence'] = pd.to_numeric(
        final_df['diabetes_prevalence'],
        errors='coerce'
    )
    final_df = final_df.dropna(subset=['diabetes_prevalence'])

    # Save processed data
    print("Saving merged data...")
    final_df.to_csv("../data/processed/state_level_merged.csv", index=False)
    print("State-level merged data saved to data/processed/state_level_merged.csv")

if __name__ == "__main__":
    print("Pre-Processing CDC diabetes data and census socioeconomics data...")
    preprocess_data()