"""
Uganda CPI / Inflation Analysis — Day 1: Load & Clean
Data source: UBOS Consumer Price Index Excel Tables, August 2026 release
(this single file contains the full history from July 2017 to August 2026)
"""

import openpyxl
import pandas as pd

# ---- CONFIG: point this at your downloaded file ----
SOURCE_FILE = "08_2026CPI_Excel_Tables_August_2026.xlsx"

wb = openpyxl.load_workbook(SOURCE_FILE, data_only=True)
ws = wb['Division ']  # note: sheet name has a trailing space in the source file

# --- Build list of (column_index, date) for every monthly column ---
max_col = ws.max_column
date_cols = []
for c in range(4, max_col + 1):
    val = ws.cell(row=1, column=c).value
    if val is not None:
        date_cols.append((c, pd.to_datetime(val).replace(day=1)))

print(f"Found {len(date_cols)} months, from {date_cols[0][1].date()} to {date_cols[-1][1].date()}")

# --- National division-level index series (rows 2-14) + Headline/Grand Total (row 15) ---
division_rows = []
for r in range(2, 15):
    name = ws.cell(row=r, column=2).value
    if name:
        division_rows.append((r, name.strip()))
division_rows.append((15, "Headline (Grand Total)"))

records = []
for r, name in division_rows:
    for c, date in date_cols:
        val = ws.cell(row=r, column=c).value
        records.append({"date": date, "division": name, "cpi_index": val})

division_df = pd.DataFrame(records)

# --- Regional centre index series (rows 51-61) ---
centre_rows = []
for r in range(51, 62):
    name = ws.cell(row=r, column=2).value
    if name:
        centre_rows.append((r, name.strip()))

records2 = []
for r, name in centre_rows:
    for c, date in date_cols:
        val = ws.cell(row=r, column=c).value
        records2.append({"date": date, "centre": name, "cpi_index": val})

regional_df = pd.DataFrame(records2)
# the "Centre" row here is UBOS's national composite shown for comparison against
# the individual towns — rename for clarity
regional_df["centre"] = regional_df["centre"].replace({"Centre": "National (composite)"})

# --- Compute year-over-year inflation for the headline series ---
headline = division_df[division_df.division == "Headline (Grand Total)"].sort_values("date").reset_index(drop=True)
headline["yoy_inflation_pct"] = headline["cpi_index"].pct_change(12) * 100

# --- Save clean outputs ---
division_df.to_csv("division_cpi_long.csv", index=False)
regional_df.to_csv("regional_cpi_long.csv", index=False)
headline.to_csv("headline_inflation.csv", index=False)

print("\nSaved: division_cpi_long.csv, regional_cpi_long.csv, headline_inflation.csv")
print("\nLatest 6 months of headline inflation:")
print(headline[["date", "cpi_index", "yoy_inflation_pct"]].tail(6).to_string(index=False))
