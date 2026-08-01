# Cement Demand Forecasting & Inventory Optimization

A machine learning and time-series forecasting solution for predicting cement demand across multiple construction sites to improve inventory planning, reduce waste, and prevent stockouts.

---

## Project Overview

Midlands Infrastructure Group (MIG) is a Tier-1 UK civil engineering and construction company operating **25–40 active project sites** nationwide.

Cement is a mission-critical material, but demand fluctuates due to changing pour schedules, weather conditions, and project progress. Existing planning relies heavily on manual forecasts and rolling construction schedules, often resulting in stock shortages, excess inventory, and expensive reactive ordering.

This project develops a data-driven forecasting and inventory optimization platform that predicts site-level cement demand up to **8 weeks ahead** and provides operational decision support through an interactive dashboard.

---

## Business Problem

MIG currently experiences:

- Cement stockouts delaying scheduled pours
- Overstocking that increases storage costs and material waste
- Expensive last-minute emergency deliveries
- Limited visibility across multiple project sites
- Manual spreadsheet-driven planning

The objective is to replace reactive inventory management with accurate demand forecasting and proactive replenishment recommendations.

---

## Project Objectives

- Forecast site-level cement demand up to **8 weeks ahead**
- Maintain **≥98% pour readiness**
- Achieve **MAPE ≤15%**
- Improve silo utilization by **20%**
- Reduce material write-offs by **30%**
- Provide real-time operational visibility through an interactive dashboard

---

# Data

The forecasting model integrates operational, logistics, inventory, and weather data.

## Operational Data

- Planned cement pours
- Daily cement consumption
- Cement type
- Site information

## Inventory & Logistics

- Opening inventory
- Daily deliveries
- Closing inventory
- Silo capacity

## External Data

- Daily rainfall
- Average temperature

---

## Data Sources

- Site weighbridge systems
- Project management systems
- Inventory management records
- Supplier delivery logs
- Weather APIs

---

## Dataset Schema

### Daily Operations

| Column | Description |
|---------|-------------|
| date | Observation date |
| site_id | Construction site identifier |
| cement_type | Cement grade |
| planned_pour_tonnes | Planned concrete pour |
| consumed_tonnes | Actual cement consumed |
| opening_inventory_tonnes | Opening stock |
| deliveries_tonnes | Deliveries received |
| closing_inventory_tonnes | Closing stock |
| rain_mm | Daily rainfall |
| avg_temp_c | Average temperature |
| silo_capacity | Site silo capacity |

### Site Metadata

| Column | Description |
|---------|-------------|
| site_id | Site identifier |
| region | Geographic region |
| silo_capacity | Maximum silo storage |
| behavior | Site demand profile |

### Cement Types

| Column |
|--------|
| cement_type |

---

# Methodology

## Data Processing

- Data cleaning and validation
- Missing value handling
- Time-series preprocessing
- Feature engineering
- Weather integration
- Site-level aggregation

---

## Forecasting

The project evaluates both statistical and machine learning forecasting approaches.

Possible models include:

- ARIMA / SARIMAX
- Random Forest
- Gradient Boosting
- XGBoost
- Other regression-based forecasting models with external regressors

Forecast horizon:

- **8 weeks ahead**

Predictors include:

- Historical consumption
- Planned pours
- Weather
- Inventory levels
- Site characteristics

---

## Inventory Optimization

Forecast outputs are translated into inventory decisions using:

- Reorder point calculations
- Safety stock estimation
- Inventory projection
- Silo capacity constraints
- Replenishment recommendations

---

# Dashboard

A Plotly Dash application provides operational visibility across all sites.

Features include:

- Demand forecasts
- Historical consumption trends
- Inventory projections
- Reorder alerts
- Silo utilization
- Site-level performance monitoring

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Database | SQLite |
| Data Processing | pandas, NumPy |
| Forecasting | scikit-learn, statsmodels |
| Visualization | Plotly, Dash |
| Version Control | Git |

---

# Project Structure

```text
.
├── data/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── inventory/
│   ├── dashboard/
│   └── utils/
├── app.py
├── requirements.txt
└── README.md
```

---

# Evaluation Metrics

The forecasting models are evaluated using metrics such as:

- Mean Absolute Percentage Error (MAPE)
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

Business performance is measured through:

- Pour readiness
- Inventory utilization
- Stockout frequency
- Material write-offs

---

# Expected Outcomes

- Accurate multi-site demand forecasting
- Improved procurement planning
- Reduced emergency deliveries
- Higher inventory utilization
- Lower material waste
- Better operational visibility across projects

---

# Future Improvements

- Automated weather data ingestion
- Supplier lead-time forecasting
- Probabilistic demand forecasting
- Real-time IoT silo monitoring
- Multi-material inventory optimization
- Cloud deployment and automated model retraining

---

## License

This project is intended for educational and portfolio purposes.