"""
Uganda CPI / Inflation Analysis — Day 2: Forecasting
Compares a seasonal-naive baseline against Holt-Winters exponential smoothing,
then forecasts the headline CPI index 6 months forward.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

headline = pd.read_csv("headline_inflation.csv", parse_dates=["date"])
headline = headline.sort_values("date").reset_index(drop=True)
series = headline.set_index("date")["cpi_index"]
series.index = pd.DatetimeIndex(series.index, freq="MS")  # monthly start frequency

# ---------- Train/test split: hold out the last 12 months ----------
n_test = 12
train, test = series[:-n_test], series[-n_test:]

# ---------- Baseline: seasonal naive (this month = same month last year) ----------
seasonal_naive_pred = train[-12:].values
seasonal_naive_pred = pd.Series(seasonal_naive_pred, index=test.index)

# ---------- Model: Holt-Winters exponential smoothing (trend + seasonality) ----------
model = ExponentialSmoothing(
    train, trend="add", seasonal="add", seasonal_periods=12
).fit()
hw_pred = model.forecast(n_test)

# ---------- Evaluate ----------
def rmse(actual, pred):
    return np.sqrt(np.mean((actual.values - pred.values) ** 2))

def mae(actual, pred):
    return np.mean(np.abs(actual.values - pred.values))

print("Evaluation on held-out last 12 months:")
print(f"  Seasonal-naive  -> RMSE: {rmse(test, seasonal_naive_pred):.3f}, MAE: {mae(test, seasonal_naive_pred):.3f}")
print(f"  Holt-Winters    -> RMSE: {rmse(test, hw_pred):.3f}, MAE: {mae(test, hw_pred):.3f}")

# ---------- Plot: actual vs both predictions on the test period ----------
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(series.index, series.values, label="Actual", color="black", linewidth=1.3)
ax.plot(test.index, seasonal_naive_pred.values, label="Seasonal-naive (test)", linestyle="--", color="grey")
ax.plot(test.index, hw_pred.values, label="Holt-Winters (test)", linestyle="--", color="#c0392b")
ax.set_title("Uganda Headline CPI: Actual vs. Forecast (held-out test period)")
ax.set_ylabel("CPI Index")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("04_forecast_evaluation.png", dpi=150)
plt.close()
print("\nSaved 04_forecast_evaluation.png")

# ---------- Refit on FULL data, forecast 6 months forward ----------
final_model = ExponentialSmoothing(
    series, trend="add", seasonal="add", seasonal_periods=12
).fit()
future_forecast = final_model.forecast(6)

print("\n6-month forward forecast (CPI index):")
print(future_forecast.to_string())

# implied YoY inflation for each forecasted month
last_year = series[-12:]
forecast_yoy = ((future_forecast.values - last_year.values[:6]) / last_year.values[:6]) * 100
print("\nImplied YoY inflation for forecasted months:")
for date, val in zip(future_forecast.index, forecast_yoy):
    print(f"  {date.strftime('%Y-%m')}: {val:.2f}%")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(series.index[-24:], series.values[-24:], label="Actual (last 24 months)", color="black")
ax.plot(future_forecast.index, future_forecast.values, label="6-month forecast", color="#2980b9", marker="o")
ax.set_title("Uganda Headline CPI: 6-Month Forward Forecast")
ax.set_ylabel("CPI Index")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("05_forecast_forward.png", dpi=150)
plt.close()
print("\nSaved 05_forecast_forward.png")
