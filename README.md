# uganda-inflation-analysis
Time-series analysis and forecasting of Uganda's Consumer Price Index (2017–2026), using official UBOS data to track inflation trends by spending category and region.

- **Forecasting**: Holt-Winters exponential smoothing substantially outperformed a seasonal-naive
  baseline on a held-out 12-month test set (RMSE 1.64 vs. 4.61; MAE 1.26 vs. 4.56 — roughly a
  65–72% reduction in error). The 6-month forward forecast projects headline inflation continuing
  to rise from 4.3% (Sept 2026) to a peak near 5.0% (Nov 2026), before easing slightly to the
  mid-4% range by early 2027.