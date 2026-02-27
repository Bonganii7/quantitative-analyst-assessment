"""
Question 4 – Two-Year Sales Forecast

Methodology:
- Reconstruct monthly active customers using First Purchase period
- Fit linear regression to cumulative customer growth
- Forecast 24 months forward
- Translate customers - food demand using average daily food per customer
- Scenario band based on slope uncertainty (±1.96 * std_err)
"""

import pandas as pd
import numpy as np
import os
from scipy.stats import linregress
import matplotlib.pyplot as plt


DATA_PATH = "../data/master_clean.csv"
OUTPUT_PATH = "../docs/question_4/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

#load

master = pd.read_csv(DATA_PATH)

#customer time series

customers = master[["cust_no", "First Purchase period"]].drop_duplicates()

# Clean YYYYMM safely
customers["fp_str"] = customers["First Purchase period"].astype(str)

customers["year"] = pd.to_numeric(customers["fp_str"].str[:4], errors="coerce")
customers["month"] = pd.to_numeric(customers["fp_str"].str[4:], errors="coerce")

customers = customers[
    customers["year"].between(2018, 2025) &
    customers["month"].between(1, 12)
].copy()

customers["date"] = pd.to_datetime(
    customers["year"].astype(int).astype(str) + "-" +
    customers["month"].astype(int).astype(str) + "-01"
)

# Monthly cumulative active customers
monthly = (
    customers
    .groupby("date")
    .size()
    .sort_index()
    .cumsum()
    .reset_index(name="active_customers")
)

monthly["t"] = np.arange(len(monthly))

#now regression

reg = linregress(monthly["t"], monthly["active_customers"])

slope = reg.slope
intercept = reg.intercept
std_err = reg.stderr
r_squared = reg.rvalue ** 2

print("\nModel Diagnostics")
print(f"Slope: {slope:.4f} customers/month")
print(f"R²: {r_squared:.4f}")
print(f"P-value: {reg.pvalue:.6f}")

#moving on to forecasting next 24 months
future_t = np.arange(len(monthly), len(monthly) + 24)

base_customers = intercept + slope * future_t
low_customers  = intercept + (slope - 1.96 * std_err) * future_t
high_customers = intercept + (slope + 1.96 * std_err) * future_t

future_dates = pd.date_range(
    monthly["date"].max() + pd.DateOffset(months=1),
    periods=24,
    freq="MS"
)

#translate to food demand

# Average daily food per customer
avg_daily_food_per_customer = (
    master.groupby("cust_no")["food portions per day"]
    .sum()
    .mean()
)

forecast_df = pd.DataFrame({
    "date": future_dates,
    "customers_base": base_customers,
    "customers_low": low_customers,
    "customers_high": high_customers
})

forecast_df["days_in_month"] = forecast_df["date"].dt.days_in_month

forecast_df["food_base"] = (
    forecast_df["customers_base"]
    * avg_daily_food_per_customer
    * forecast_df["days_in_month"]
)

forecast_df["food_low"] = (
    forecast_df["customers_low"]
    * avg_daily_food_per_customer
    * forecast_df["days_in_month"]
)

forecast_df["food_high"] = (
    forecast_df["customers_high"]
    * avg_daily_food_per_customer
    * forecast_df["days_in_month"]
)

forecast_df.to_csv(OUTPUT_PATH + "q4_forecast.csv", index=False)


# VISUALISATION (Historical + Forecast)
# ============================================================

plt.figure(figsize=(10, 5))

# Historical
plt.plot(monthly["date"],
         monthly["active_customers"],
         label="Historical Customers",
         color="#1F4E79")

# Forecast
plt.plot(future_dates,
         base_customers,
         label="Forecast (Base)",
         color="#E67E22")

plt.plot(future_dates,
         low_customers,
         linestyle="--",
         color="#7D3C98",
         label="Low Scenario")

plt.plot(future_dates,
         high_customers,
         linestyle="--",
         color="#2E86C1",
         label="High Scenario")

plt.title("Customer Growth Forecast – 24 Months")
plt.xlabel("Date")
plt.ylabel("Active Customers")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "q4_forecast.png")
plt.close()



#report findings
# ============================================================

# Compute yearly totals
year1_total = forecast_df["food_base"].iloc[:12].sum()
year2_total = forecast_df["food_base"].iloc[12:24].sum()

with open(OUTPUT_PATH + "q4_report.md", "w") as f:

    f.write("# Question 4 Two-Year Sales Forecast\n\n")

    f.write("## Baseline (Latest Historical Period)\n\n")
    f.write(
        f"- Latest Active Customers: {monthly['active_customers'].iloc[-1]:.0f}\n"
        f"- Average Daily Food per Customer: {avg_daily_food_per_customer:.2f} portions\n"
        f"- Model R^2: {r_squared:.4f}\n\n"
    )

    f.write("## Forecast Methodology\n\n")
    f.write(
        "- Linear regression fitted to cumulative monthly active customers\n"
        "- Forecast: 24 months\n"
        "- Scenario bands: slope +/- 1.96 x standard error\n"
        "- Monthly food demand = Customers x Avg Daily Food x Days in Month\n\n"
    )

    f.write("## Two-Year Projection, The BAse\n\n")
    f.write(
        f"- Year 1 Forecast Total: {year1_total:,.0f} portions\n"
        f"- Year 2 Forecast Total: {year2_total:,.0f} portions\n\n"
    )

    f.write("## Internal Factors\n\n")
    f.write(
        "- Historical customer acquisition trend\n"
        "- Current insect ownership distribution\n"
        "- Average food demand per customer\n"
        "- Stability of biological feeding requirements\n\n"
    )

    f.write("## External Factors Not modelled(Limitations) \n\n")
    f.write(
        "- Inflation and feed cost pressures\n"
        "- Economic conditions affecting hobby spending\n"
        "- Supplier reliability and logistics\n"
        "- Regulatory considerations for exotic pets\n\n"
    )

    f.write("## Key Assumptions\n\n")
    f.write(
        "- Linear customer growth continues over forecast horizon\n"
        "- No churn modelled\n"
        "- Average daily food per customer remains stable\n"
        "- No structural shift in insect ownership behaviour\n"
    )

print("Q4 markdown report saved.")

print("\nQ4 forecast completed successfully.")
