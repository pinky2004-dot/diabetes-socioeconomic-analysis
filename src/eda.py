import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# =====================================================
# 1. Data Loading & Validation
# =====================================================

def load_data():
    """Load and validate processed dataset"""
    try:
        df = pd.read_csv("../data/processed/final_dataset.csv")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

# =====================================================
# 2. Hypothesis Testing Functions
# =====================================================

def hypothesis_1_poverty_diabetes(df):
    """H1: Poverty correlates with diabetes prevalence"""
    # Pearson correlation
    corr, pval = stats.pearsonr(df['poverty_population'], 
                               df['diabetes_prevalence'])
    print(f"\n[H1] Poverty-Diabetes Correlation: {corr:.3f} (p={pval:.4f})")
    
    # Interactive scatter plot
    fig = px.scatter(
        df, 
        x='poverty_population', 
        y='diabetes_prevalence',
        trendline='ols',
        hover_data=['county', 'state', 'is_rural'],
        title='H1: Poverty vs Diabetes Prevalence',
        labels={
            'poverty_population': 'People in Poverty',
            'diabetes_prevalence': 'Diabetes (%)'
        },
        color='is_rural',
        width=1200,
        height=600
    )
    fig.write_html("../reports/h1_poverty_scatter.html")

def hypothesis_2_food_deserts(df):
    """H2: Food deserts have higher diabetes rates"""
    # Create food desert flag (top 25% of low-access tracts)
    threshold = df['LA1and10'].quantile(0.75)
    df['food_desert'] = np.where(df['LA1and10'] >= threshold, 1, 0)
    
    # T-test
    desert = df[df['food_desert'] == 1]['diabetes_prevalence']
    non_desert = df[df['food_desert'] == 0]['diabetes_prevalence']
    t_stat, pval = stats.ttest_ind(desert, non_desert)
    print(f"\n[H2] Food Desert T-Test: t={t_stat:.2f} (p={pval:.4f})")
    
    # Box plot with marginal distributions
    fig = px.scatter(
        df,
        x='LA1and10',
        y='diabetes_prevalence',
        color='food_desert',
        marginal_x='histogram',
        marginal_y='box',
        title='H2: Food Desert Tracts vs Diabetes Prevalence',
        labels={
            'LA1and10': 'Low-Access Tracts',
            'diabetes_prevalence': 'Diabetes (%)'
        },
        width=1200,
        height=600
    )
    fig.write_html("../reports/h2_food_desert.html")

def hypothesis_3_rural_urban(df):
    """H3: Rural areas have worse diabetes outcomes"""
    # T-test
    rural = df[df['is_rural'] == 1]['diabetes_prevalence']
    urban = df[df['is_rural'] == 0]['diabetes_prevalence']
    t_stat, pval = stats.ttest_ind(rural, urban)
    print(f"\n[H3] Rural-Urban T-Test: t={t_stat:.2f} (p={pval:.4f})")
    
    # Interactive choropleth
    fig = px.choropleth(
        df,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations='FIPS',
        color='diabetes_prevalence',
        scope='usa',
        hover_data=['county', 'state', 'is_rural'],
        color_continuous_scale='Viridis',
        title='Diabetes Prevalence by County',
        width=1200,
        height=600
    )
    fig.update_traces(marker_line_width=0.2, marker_line_color='gray')
    fig.write_html("../reports/h3_choropleth.html")

# =====================================================
# 3. Main Execution
# =====================================================

if __name__ == "__main__":
    df = load_data()
    print(df.info())
    
    print("="*40)
    print("Dataset Overview:")
    print(f"Total counties: {len(df)}")
    print(f"Diabetes range: {df['diabetes_prevalence'].min():.1f}% - {df['diabetes_prevalence'].max():.1f}%")
    print(f"Rural counties: {df['is_rural'].sum()} ({df['is_rural'].mean():.1%})")
    print("\nKey Correlations:")
    print(df[['diabetes_prevalence', 'poverty_population', 'LA1and10']].corr())
    
    hypothesis_1_poverty_diabetes(df)
    hypothesis_2_food_deserts(df)
    hypothesis_3_rural_urban(df)
    
    print("\nVisualizations saved to reports/ directory")