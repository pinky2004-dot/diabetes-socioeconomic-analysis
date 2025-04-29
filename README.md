# Impact of Socioeconomic Factors on Diabetes Prevalence in the US 

## Domain: Public Health / Epidemiology 

### 1. Hypotheses 

- H1: Counties with higher poverty rates have higher diabetes prevalence. 
- H2: Food deserts (low access to healthy food) correlate with elevated diabetes rates. 
- H3: Rural counties experience worse diabetes outcomes due to limited healthcare access. 

### 2. Data Collection 

#### Sources: 

- Diabetes Prevalence: CDC’s Diabetes Surveillance System (county-level data). 
- Socioeconomic Data: U.S. Census Bureau (poverty rates, median income). 
- Food Access: USDA Food Environment Atlas (food desert classifications).

#### Data Processing:

- Merge datasets using county FIPS codes. 
- Clean missing values and standardize metrics (e.g., diabetes rate per 100k residents).

### 3. Exploratory Data Analysis (EDA) 

- Calculate summary statistics (mean diabetes rate, poverty rate distributions). 
- Preliminary visualizations: 

### 4. Tools & Code 

- Python Libraries:
    - Pandas for data merging. 
    - Plotly for interactive charts. 
    - GeoPandas for map visualizations. 

### 5. Expected Insights 

- Policymakers can prioritize interventions in high-risk counties. 
- Public health campaigns can target food deserts and rural clinics. 

### Why This Works 

- Relevance: Diabetes is a critical global health issue with clear ties to socioeconomic factors. 
- Data Accessibility: All datasets are publicly available. 
- Interactivity: Engages users to explore complex relationships (e.g., "Does poverty cause diabetes, or is it mediated by food access?"). 
- Scalability: Expandable to other diseases (e.g., hypertension) or global datasets. 
