# Enterprise Demand Forecasting & Inventory Optimization

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-Data%20Analysis-yellow)
![SQL](https://img.shields.io/badge/SQL-Analytics-blue)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-orange)

**Live Dashboard:** https://public.tableau.com/app/profile/rishav.sharma8845/viz/Book1_17804260705190/Dashboard

## 📌 Project Objective
To build an end-to-end demand forecasting engine that predicts daily unit sales for retail products. This project tackles the classic supply chain problem of inventory optimization, aiming to reduce the holding costs of overstocking while minimizing revenue loss from stockouts.

## 🛠️ Tech Stack
* **Data Engineering & Database:** Python (Pandas), SQLite, ANSI SQL
* **Predictive Modeling:** Python (Statsmodels, Holt-Winters Exponential Smoothing)
* **Business Intelligence:** Tableau

---

## 🏗️ Phase 1: Data Engineering & SQL Architecture

The raw dataset contained over 1,900 individual day columns for sales, violating standard database First Normal Form. 

* **ETL Pipeline:** Engineered a memory-safe Python pipeline to unpivot (melt) the wide data into a vertical format, processing ~58.5 million rows in 500,000-row chunks to prevent system memory failure.
* **Database Construction:** Built a localized SQLite Star Schema database consisting of a core fact table (`fact_sales`) and dimensional tables (`dim_calendar`, `dim_sell_prices`).

### Highlighted SQL: Promotional Impact Analysis
Below is an example of the analytical SQL used to aggregate 58 million rows and evaluate the impact of SNAP benefit days on overall supply chain volume:

```sql
SELECT 
    c.snap_CA AS SNAP_Benefit_Day,
    ROUND(AVG(f.units_sold), 2) AS Avg_Daily_Units_Sold,
    SUM(f.units_sold) AS Total_Volume
FROM fact_sales f
INNER JOIN dim_calendar c ON f.date_id = c.date_id
GROUP BY c.snap_CA
ORDER BY Total_Volume DESC;

## 📈 Phase 2: Predictive Modeling
Before applying advanced forecasting, I established a strict business baseline using a 30-day moving average. I then applied a Holt-Winters Exponential Smoothing model to capture the heavy 7-day weekly seasonality inherent in retail supply chains.

Baseline Model (30-Day MA) RMSE: 5,824 units

Advanced Model (Holt-Winters) RMSE: 3,296 units

Business Impact: The advanced model successfully reduced the forecasting error by 43.39%. In a production environment, this drastically tightens inventory thresholds, directly lowering warehouse holding costs.

## 📊 Phase 3: Stakeholder Dashboarding
Translated the complex mathematical outputs into a commercial operational tool using Tableau. The dashboard provides supply chain directors with:

An executive summary of projected future volume.

A continuous time-series overlay of historical actuals vs. out-of-sample forecasts.

An automated tactical exception matrix flagging immediate overstock and stockout risks.


---
## Repository Structure
```
supply-chain-demand-forecasting/
│
├── notebooks/
│   ├── 01_etl_unpivot.ipynb
│   ├── 02_db_ingestion.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   └── 04_predictive_modeling.ipynb
│
├── sql_scripts/
│   ├── 01_create_tables.sql
│   └── 02_analytical_queries.sql
│
├── pipelines/
│   ├── run_pipeline.py
│   └── verify_db.py
│
├── Dashboard ss.png
├── .gitignore
├── LICENSE
└── README.md
