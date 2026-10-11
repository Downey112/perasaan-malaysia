# Perasaan Malaysia ⛅🇲🇾

[![Daily Sync Status](https://github.com/Downey112/perasaan-malaysia/actions/workflows/perasaan_sync.yml/badge.svg)](https://github.com/Downey112/perasaan-malaysia/actions/workflows/perasaan_sync.yml)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Data Source: data.gov.my](https://img.shields.io/badge/Data-data.gov.my-00A3E0?style=flat)](https://data.gov.my)
[![Destination: Google Sheets](https://img.shields.io/badge/Storage-Google_Sheets-34A853?style=flat&logo=googlesheets&logoColor=white)](https://developers.google.com/sheets/api)

An automated daily ETL pipeline that extracts 7-day weather forecasts across Malaysian states and districts from the official **MetMalaysia open data API (`data.gov.my`)** and synchronizes structured records into Google Sheets / Looker Studio for reporting.

---

## ⚡ Architecture & Automation

```mermaid
flowchart LR
    A["data.gov.my API<br/>(MetMalaysia Forecast)"] -->|Daily at 06:00 AM MYT| B["GitHub Actions Cron"]
    B --> C["Python ETL<br/>(src/extractor.py)"]
    C -->|Validate & Transform| D["Structured DataFrame<br/>(pandas)"]
    D -->|Upsert Rolling 7-Day Forecast| E["Google Sheets / Cloud<br/>(gspread Service Account)"]
    E --> F["Google Looker Studio<br/>(Reporting & Geospatial BI)"]
```

* **Orchestration:** GitHub Actions scheduled cron job (`.github/workflows/perasaan_sync.yml`) runs automatically every morning at 06:00 AM MYT (22:00 UTC), with manual trigger support (`workflow_dispatch`).
* **Ingestion:** Queries the official government weather endpoint (`https://api.data.gov.my/weather/forecast`), parsing multi-level location hierarchies (State `St` and District `Ds`).
* **Transformation:** Flattens JSON payloads into standardized relational records (morning/afternoon/night weather summaries, min/max temperatures, date tokens).
* **Storage & Access:** Authenticates using Google Cloud Service Account credentials (`gspread`) to refresh the reporting worksheet.

---

## 🗄️ Extracted Schema

| Field | Data Type | Description |
|---|---|---|
| `Extraction_Date` | Date (`YYYY-MM-DD`) | Timestamp when the ETL job ran |
| `Location_ID` | String | Official administrative identifier (`St*` for State, `Ds*` for District) |
| `Location_Name` | String | Name of the administrative district, city, or territory |
| `Location_Type` | Categorical | Classification level (`State` or `District`) |
| `Forecast_Date` | Date (`YYYY-MM-DD`) | Target forecast date |
| `Morning_Forecast` | String | Weather forecast during morning hours |
| `Afternoon_Forecast` | String | Weather forecast during afternoon peak heat |
| `Night_Forecast` | String | Weather forecast during evening/night |
| `Summary_Forecast` | String | Primary consolidated daily weather classification |
| `Min_Temp_C` | Float | Forecasted minimum temperature (°C) |
| `Max_Temp_C` | Float | Forecasted maximum daily temperature (°C) |

---

## 📁 Repository Structure

```text
perasaan-malaysia/
├── .github/
│   └── workflows/
│       └── perasaan_sync.yml      # GitHub Actions scheduled cron workflow (06:00 AM MYT)
├── src/
│   └── extractor.py               # MetMalaysia API ingestion & Google Sheets synchronization
├── credentials.json               # Local GCP service account (git-ignored)
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Git tracking exclusions
└── README.md                      # Project documentation
```

---

## ⚙️ Local Development & Setup

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/Downey112/perasaan-malaysia.git
cd perasaan-malaysia

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Service Account Credentials
Place your Google Cloud Service Account JSON file as `credentials.json` in the root directory (already excluded via `.gitignore`), or export it to the environment:
```bash
export GCP_SA_KEY='{"type": "service_account", ...}'
```

### 3. Run Pipeline Manually
```bash
python src/extractor.py
```
