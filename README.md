# 🇲🇾 Perasaan Malaysia: MetMalaysia Climate Forecast Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](#)
[![GitHub Actions](https://img.shields.io/badge/Workflow-GitHub%20Actions-2088FF.svg?logo=github-actions&logoColor=white)](#)
[![Looker Studio](https://img.shields.io/badge/BI-Looker%20Studio-F4B400.svg?logo=google&logoColor=white)](#)
[![Data Source](https://img.shields.io/badge/Data%20Source-MetMalaysia%20API-00897B.svg)](#)

An automated end-to-end data pipeline that extracts, cleans, and visualizes official 7-day climate forecasts from the Malaysian Meteorological Department (MetMalaysia). The system uses scheduled workflow orchestration to ingest API records, applies spatial and temporal transformations, and serves the dataset into an interactive business intelligence dashboard.

---

## 📊 Live Interactive Dashboard

**[👉 Launch the Live Interactive Looker Studio Report](PASTE_YOUR_PUBLIC_LINK_HERE)**

<p align="center">
  <a href="https://datastudio.google.com/reporting/e7474503-e4f5-45e7-a575-31aebc284a85">
    <img width="1218" height="916" alt="dashboard" src="https://github.com/user-attachments/assets/560713b0-e027-4a30-966e-560f62b360dc" />

  </a>
</p>

---

## 🏗️ System Architecture & Pipeline Flow

```text
┌────────────────────────────────┐
│   MetMalaysia Forecast API     │  Official REST API endpoint
└───────────────┬────────────────┘
                │
                ▼ (Daily cron trigger at 06:00 MYT)
┌────────────────────────────────┐
│     GitHub Actions Runner      │  Automated workflow orchestration
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   Python Extraction & ETL      │  Flattens nested JSON, casts data types,
│     (Pandas / Requests)        │  engineers 'Location_Full_Name' geo-string
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│    Cloud Database / Storage    │  Stores current 7-day forecast records
└───────────────┬────────────────┘
                │
                ▼ (Automated data sync)
┌────────────────────────────────┐
│      Looker Studio Report      │  Bubble Map, Probability Matrix, Heatmap
└────────────────────────────────┘
```

1. **Extraction (Scheduled Ingestion):**
   * A GitHub Actions cron workflow executes daily at 06:00 MYT.
   * Fetches the 7-day weather forecast directly from the MetMalaysia official open data endpoint.
2. **Transformation (Data Cleansing & Geo-Engineering):**
   * **JSON Flattening:** Unpacks nested forecasts (morning, afternoon, night, summary) into structured tabular records.
   * **Spatial Concatenation:** Generates a synthetic geographical dimension `Location_Full_Name` using the formula `CONCAT(Location_Name, ", Malaysia")` to prevent Google Maps district ambiguity and rendering gaps.
   * **Schema Standardization:** Casts dates to `YYYY-MM-DD` and temperature metrics to numerical floats/integers.
3. **Loading:**
   * Overwrites the live database table to maintain an exact, rolling 7-day forecast horizon.
4. **Presentation:**
   * Direct connection to Google Looker Studio with real-time field aggregation and cross-filtering controls.

---

## 🗄️ Data Dictionary

| Field Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `Location_Name` | Text | Name of the administrative district, city, or territory | `Kubang Pasu`, `Kota Bharu` |
| `Location_Type` | Text | Classification level of the region | `State`, `District` |
| `Location_Full_Name` | Geo | Engineered location string for geospatial rendering | `Kubang Pasu, Malaysia` |
| `Forecast_Date` | Date | Date corresponding to the daily forecast (`YYYY-MM-DD`) | `2026-09-24` |
| `Morning_Forecast` | Text | Forecasted conditions during morning hours | `Cerah`, `Hujan di satu dua tempat` |
| `Afternoon_Forecast`| Text | Forecasted conditions during afternoon peak heat | `Ribut petir di beberapa tempat` |
| `Summary_Forecast`  | Text | Primary overall weather condition for the day | `Hujan`, `Tiada Hujan` |
| `Max_Temp_C`        | Number | Expected maximum daily temperature in Celsius | `34` |

---

## 📈 Dashboard Component Breakdown

The front-end business intelligence interface consists of three distinct analytical modules:

* **Geospatial Anchor (Bubble Map):** 
  * Plots every district using the computed `Location_Full_Name`.
  * Encodes district temperature using an aggregated color scale (`Average` of `Max_Temp_C`) to immediately surface regional heat islands.
  * Interactive tooltips display afternoon weather outlooks upon hover.
* **Weather Probability Distribution (100% Stacked Column Chart):**
  * Displays the proportional breakdown of forecasted weather types across districts.
  * X-axis tracks `Location_Name`, broken down by `Afternoon_Forecast` with an aggregation metric of `Record Count`.
  * Visual limits set to eliminate default "Others" bucket truncation, ensuring full national visibility.
* **Hierarchical Temperature Matrix (Pivot Table with Heatmap):**
  * Hierarchical drill-down tracking temperature transitions across the 7-day horizon.
  * Rows: `Location_Type` (State) → `Location_Name` (District).
  * Columns: `Forecast_Date` sorted chronologically in ascending order.
  * Metric: `AVG(Max_Temp_C)` highlighted using a multi-point gradient heatmap.

---

## 📁 Repository Structure

```text
perasaan-malaysia/
├── .github/
│   └── workflows/
│       └── daily_etl.yml          # GitHub Actions scheduled workflow
├── data/                          # Cached data snapshots (if applicable)
├── scripts/
│   ├── extract.py                 # MetMalaysia API ingestion script
│   └── transform_load.py          # Data cleansing, geo-formatting, DB load
├── assets/
│   └── dashboard_preview.png      # High-resolution dashboard screenshot
├── requirements.txt               # Python package dependencies
├── .env.example                   # Safe template for local credentials
├── .gitignore                     # Git tracking exclusions
└── README.md                      # Project documentation
```

---

## ⚙️ Local Setup & Execution

### Prerequisites
* Python 3.10 or higher
* Valid database connection credentials 

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/perasaan-malaysia.git](https://github.com/your-username/perasaan-malaysia.git)
cd perasaan-malaysia
```

### 2. Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Credentials
**Never commit your real database credentials.** Ensure `.env` is listed in your `.gitignore` file. 

The repository includes an `.env.example` file as a safe template:

```env
# .env.example
DB_HOST=localhost
DB_PORT=5432
DB_USER=
DB_PASSWORD=
DB_NAME=
```
To run the pipeline locally, copy `.env.example`, rename the new file to `.env`, and fill in your actual private database credentials.

### 4. Run the Pipeline
```bash
python scripts/extract.py
python scripts/transform_load.py
```
