"""
Uganda CPI / Inflation Analysis — Day 1: EDA
Reads the CSVs produced by 01_load_clean.py and produces three charts.
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. Headline inflation trend over the full history ----------
headline = pd.read_csv("headline_inflation.csv", parse_dates=["date"])

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(headline["date"], headline["yoy_inflation_pct"], color="#c0392b", linewidth=1.5)
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_title("Uganda Year-over-Year Inflation, July 2018 – August 2026")
ax.set_ylabel("YoY Inflation (%)")
ax.set_xlabel("Date")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("01_headline_inflation_trend.png", dpi=150)
plt.close()
print("Saved 01_headline_inflation_trend.png")

# ---------- 2. Division-level breakdown: which categories moved most recently ----------
division_df = pd.read_csv("division_cpi_long.csv", parse_dates=["date"])
division_df = division_df[division_df.division != "Headline (Grand Total)"]

# YoY inflation per division
division_df = division_df.sort_values(["division", "date"])
division_df["yoy_pct"] = division_df.groupby("division")["cpi_index"].pct_change(12) * 100

latest_date = division_df["date"].max()
latest_by_division = (
    division_df[division_df["date"] == latest_date]
    .sort_values("yoy_pct", ascending=True)
)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(latest_by_division["division"], latest_by_division["yoy_pct"], color="#2980b9")
ax.set_title(f"YoY Inflation by Spending Category — {latest_date.strftime('%B %Y')}")
ax.set_xlabel("YoY Inflation (%)")
ax.axvline(0, color="grey", linewidth=0.8)
plt.tight_layout()
plt.savefig("02_division_breakdown.png", dpi=150)
plt.close()
print("Saved 02_division_breakdown.png")
print("\nDivision breakdown, most recent month:")
print(latest_by_division[["division", "yoy_pct"]].to_string(index=False))

# ---------- 3. Regional comparison: is Kampala inflating faster than upcountry? ----------
regional_df = pd.read_csv("regional_cpi_long.csv", parse_dates=["date"])
regional_df = regional_df.sort_values(["centre", "date"])
regional_df["yoy_pct"] = regional_df.groupby("centre")["cpi_index"].pct_change(12) * 100

fig, ax = plt.subplots(figsize=(12, 6))
for centre, grp in regional_df.groupby("centre"):
    ax.plot(grp["date"], grp["yoy_pct"], label=centre, linewidth=1.2)
ax.set_title("YoY Inflation by Town/Region")
ax.set_ylabel("YoY Inflation (%)")
ax.legend(fontsize=8, ncol=2)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("03_regional_comparison.png", dpi=150)
plt.close()
print("\nSaved 03_regional_comparison.png")

latest_regional = regional_df[regional_df["date"] == regional_df["date"].max()].sort_values("yoy_pct", ascending=False)
print(f"\nRegional inflation ranking, {regional_df['date'].max().strftime('%B %Y')}:")
print(latest_regional[["centre", "yoy_pct"]].to_string(index=False))
