# Project Title: Impact of Socioeconomic Factors on Diabetes Prevalence in the US 

## Domain: Public Health / Epidemiology 

# 1. Data Collection 

### Sources: 
- Diabetes Prevalence: CDC’s Diabetes Surveillance System (county-level data). 
- Socioeconomic Data: U.S. Census Bureau (poverty rates, median income). 
- Food Access: USDA Food Environment Atlas (food desert classifications). 
- Healthcare Access: HRSA’s Health Center Program (clinics per capita).
Data Processing:
- Merge datasets using county FIPS codes. 
- Clean missing values and standardize metrics (e.g., diabetes rate per 100k residents).

# 2. Hypotheses 

- H1: Counties with higher poverty rates have higher diabetes prevalence. 
- H2: Food deserts (low access to healthy food) correlate with elevated diabetes rates. 
- H3: Rural counties experience worse diabetes outcomes due to limited healthcare access. 

# 3. Exploratory Data Analysis (EDA) 

- Calculate summary statistics (mean diabetes rate, poverty rate distributions). 
- Preliminary visualizations: 
    - Scatter plot of poverty rate vs. diabetes rate. 
    - Boxplot comparing urban vs. rural diabetes rates. 
    - Correlation matrix of variables (diabetes, poverty, food access, clinics per capita). 

# 4. Interactive Visualizations 

## Tools: Python (Plotly, GeoPandas), Tableau. 

## Choropleth Map:
    - Layered map showing diabetes prevalence (color) and food deserts (overlay markers).	
    - Toggle layers (poverty/food access). 
    - Hover for county details (rate, population). 

## Scatter Plot Matrix:
    - Explore correlations between diabetes, poverty, food access, and healthcare.
    - Brush to highlight outliers. 
    - Tooltip with county name and exact values. 

## Time-Series Line Chart:
    - Diabetes trends (2010–2020) compared to policy changes (e.g., ACA rollout).
    - Slider to select years. 
    - Annotate policy milestones. 

## Bar Chart:
    - Compare urban vs. rural diabetes rates and clinic availability.
    - Filter by region (Northeast, South, etc.). 

# 5. Design Rationale 

- Choropleth Maps: Ideal for spatial patterns; diverging color scales highlight high/low risk areas.
- Scatter Plots: Reveal non-linear relationships (e.g., diabetes vs. income). 
- Interactivity: Enables users to explore "why" behind patterns (e.g., drilling into rural counties). 
- Color Choices: Red (high risk) to green (low risk) for intuitive interpretation. 

# 6. Tools & Code 

- Python Libraries:
    - Pandas for data merging. 
    - Plotly for interactive charts. 
    - GeoPandas for map visualizations. 
- Bonus: Use Dash to build a web dashboard integrating all visualizations. 

# 7. Expected Insights 

- Policymakers can prioritize interventions in high-risk counties. 
- Public health campaigns can target food deserts and rural clinics. 

# Why This Works 

- Relevance: Diabetes is a critical global health issue with clear ties to socioeconomic factors. 
- Data Accessibility: All datasets are publicly available and mergeable. 
- Interactivity: Engages users to explore complex relationships (e.g., "Does poverty cause diabetes, or is it mediated by food access?"). 
- Scalability: Expandable to other diseases (e.g., hypertension) or global datasets. 
