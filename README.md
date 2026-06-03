# Enterprise Demand Forecasting & Inventory Optimization

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-Data%20Engineering%20&%20Modeling-yellow)
![SQL](https://img.shields.io/badge/SQL-Database%20Architecture-blue)
![Tableau](https://img.shields.io/badge/Tableau-Supply%20Chain%20BI-orange)

**Live Dashboard:** [View Interactive Tableau Dashboard Here](https://public.tableau.com/app/profile/rishav.sharma8845/viz/Book1_17804260705190/Dashboard)

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

```

## 📈 Phase 2: Predictive Modeling 
Before applying advanced forecasting, I established a strict business baseline using a 30-day moving average. I then applied a Holt-Winters Exponential Smoothing model to capture the heavy 7-day weekly seasonality inherent in retail supply chains.

* **Baseline Model (30-Day MA) RMSE:** 5,824 units

* **Advanced Model (Holt-Winters) RMSE:** 3,296 units

* **Business Impact:** The advanced model successfully reduced the forecasting error by 43.39%. In a production environment, this drastically tightens inventory thresholds, directly lowering warehouse holding costs.

---

## 📊 Phase 3: Stakeholder Dashboarding
Translated the complex mathematical outputs into a commercial operational tool using Tableau. The dashboard provides supply chain directors with:

An executive summary of projected future volume.

A continuous time-series overlay of historical actuals vs. out-of-sample forecasts.

An automated tactical exception matrix flagging immediate overstock and stockout risks.

---
## Repository Structure
```
supply-chain-demand-forecasting/
├── notebooks/
│   ├── 01_etl_unpivot.ipynb
│   ├── 02_db_ingestion.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   └── 04_predictive_modeling.ipynb
├── sql_scripts/
│   ├── 01_create_tables.sql
│   └── 02_analytical_queries.sql
├── pipelines/
│   ├── run_pipeline.py
│   └── verify_db.py
├── Dashboard ss.png
├── .gitignore
├── LICENSE
└── README.md

```

## 🚀 How to Run the Project

### 1. Prerequisites & Environment Setup
Ensure you have Python 3.8+ installed. Clone this repository and set up your virtual environment:

```bash
git clone https://github.com/Rishav-20/supply-chain-demand-forecasting.git
cd supply-chain-demand-forecasting
python -m venv venv
source venv/Scripts/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Execute the Data Pipeline
Run the master orchestration script to execute the data processing, unpivoting, database construction, and schema verification sequentially:

```bash
python pipelines/run_pipeline.py
```

### 3. Review Models & Analytical View
Open Jupyter Notebook to explore the predictive modeling architecture or run the SQL scripts directly against the generated SQLite database:

```bash
jupyter notebook notebooks/04_predictive_modeling.ipynb
```

## 🔮 Future Improvements

While the core data architecture and forecasting engine are fully operational, the following enhancements would scale this project for an enterprise production environment:

1. **Cloud-Native Ingestion (Scalability):** Migrate the local SQLite database to a cloud data warehouse like Google BigQuery or Snowflake. This would allow the ingestion pipeline to scale from 58 million rows to billions of transaction records seamlessly.
2. **Feature Engineering for Promotional Events (Accuracy):** Integrate additional exogenous variables into the predictive models—such as localized weather patterns, retail discount tracking, and competitor pricing dynamics—to reduce the RMSE further on highly volatile promotional days.
3. **Automated MLOps Pipeline (Orchestration):** Wrap the current Python execution pipeline into a containerized workflow using Docker and orchestrate it with Apache Airflow to schedule daily model retraining and automated dashboard refreshes.
