# Uganda Inflation Analysis (2017–2026)

A time-series analysis of Uganda's Consumer Price Index (CPI), using official monthly data from the Uganda Bureau of Statistics (UBOS) to explore inflation trends by spending category and region, and to forecast where inflation is headed.

## Data Source

Uganda Bureau of Statistics (UBOS) — [Consumer Price Index Excel Tables](https://www.ubos.org), August 2026 release. This single release contains the complete monthly CPI series from **July 2017 to August 2026** across:
- 13 COICOP spending categories (Food, Transport, Housing, Health, etc.)
- 10 regional town/city baskets (Kampala High/Middle/Low Income, Jinja, Mbale, Gulu, Arua, Masaka, Mbarara, Fort Portal)

## Project Structure

```
├── 01_load_clean.py       # Extracts and cleans raw UBOS Excel tables into tidy CSVs
├── 02_eda.py               # Exploratory analysis: trend, category breakdown, regional comparison
├── 03_forecast.py          # Time-series forecasting (Holt-Winters vs. seasonal-naive baseline)
├── division_cpi_long.csv   # Cleaned: CPI index by spending category over time
├── regional_cpi_long.csv   # Cleaned: CPI index by region/town over time
├── headline_inflation.csv  # Cleaned: national headline CPI index + YoY inflation
└── *.png                   # Generated charts
```

## Methodology

1. **Extraction**: Parsed UBOS's multi-section Excel workbook (index levels, annual % change, monthly % change, national and regional breakdowns) into tidy long-format CSVs suitable for analysis.
2. **Validation**: Cross-checked computed year-over-year inflation against UBOS's own published press-release figures (e.g. July 2025: 3.8% published vs. 3.76% computed) to confirm extraction accuracy.
3. **Exploratory analysis**: Examined the national inflation trend, decomposed it by spending category, and compared regional cost-of-living trajectories.
4. **Forecasting**: Compared a seasonal-naive baseline against Holt-Winters exponential smoothing (trend + seasonality) on a held-out 12-month test period, then produced a 6-month forward forecast.

## Key Findings

- Uganda's headline inflation rose from **2.8% (March 2026) to 4.1% (August 2026)**.
- This rise is **concentrated, not broad-based**: Insurance & Financial Services (+10.1% YoY) and Transport (+9.4% YoY) are the dominant drivers, while Food and Non-Alcoholic Beverages — typically the primary inflation driver in the region — sits close to the national average at 3.6%.
- Regionally, **Kampala's high-income basket (4.9%) is inflating faster than its low-income basket (4.1%)** — a pattern consistent with wealthier households' greater relative exposure to transport and financial-service costs, which are the categories driving the current increase.
- *(Forecast results — fill in after running `03_forecast.py`: model accuracy vs. baseline, and the 6-month forward projection.)*

## How to Run

```bash
pip install pandas openpyxl matplotlib statsmodels

python 01_load_clean.py    # produces the three cleaned CSVs
python 02_eda.py           # produces trend/category/regional charts
python 03_forecast.py      # produces forecast evaluation + 6-month projection
```

## Tech Stack

Python · pandas · openpyxl · matplotlib · statsmodels

## Author

Ssali Remigius Kiggundu ([@Ssali-Remy](https://github.com/Ssali-Remy))