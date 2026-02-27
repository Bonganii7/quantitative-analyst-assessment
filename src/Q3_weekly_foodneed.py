"""
Weekly Food Requirement
and for perion 1 April 2020 – 1 August 2020

"""

import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt


DATA_PATH = "../data/master_clean.csv"
OUTPUT_PATH = "../docs/question_3/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

#load data

master = pd.read_csv(DATA_PATH)

if "food portions per day" not in master.columns:
    raise ValueError("Column 'food portions per day' not found.")

#demand

# Each row = one insect
total_daily_food = master["food portions per day"].sum()

#period
start_date = datetime(2020, 4, 1)
end_date = datetime(2020, 8, 1)

total_days = (end_date - start_date).days

#weekly schedule
weeks = []
current = start_date
week_num = 1

while current < end_date:
    week_end = min(current + pd.Timedelta(days=7), end_date)
    days_in_week = (week_end - current).days

    food_required = total_daily_food * days_in_week

    weeks.append({
        "Week": week_num,
        "Start Date": current.date(),
        "End Date": week_end.date(),
        "Days": days_in_week,
        "Food Required": round(food_required, 2)
    })

    current = week_end
    week_num += 1

weekly_schedule = pd.DataFrame(weeks)

# Save schedule
weekly_schedule.to_csv(OUTPUT_PATH + "q3_weekly_schedule.csv", index=False)

#vis

plt.figure(figsize=(10, 5))


# Colour final partial week differently
colors = ["#2E86C1"] * (len(weekly_schedule) - 1) + ["#E74C3C"]


plt.bar(
    weekly_schedule["Week"],
    weekly_schedule["Food Required"],
    color=colors
)


plt.title("Weekly Food Requirement (Apr–Aug 2020)")
plt.xlabel("Week Number")
plt.ylabel("Food Portions")
plt.xticks(weekly_schedule["Week"])


# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2E86C1", label="Full Week (7 days)"),
    Patch(facecolor="#E74C3C", label="Partial Final Week (3 days)")
]
plt.legend(handles=legend_elements)


plt.tight_layout()
plt.savefig(OUTPUT_PATH + "q3_weekly_chart.png")
plt.close()


# ============================================================
# REPORT
# ============================================================

with open(OUTPUT_PATH + "q3_report.md", "w") as f:

    f.write("# Question 3 – Weekly Food Requirement\n\n")

    f.write("## Period Overview\n\n")
    f.write(
        f"- Start Date: {start_date.date()}\n"
        f"- End Date: {end_date.date()}\n"
        f"- Total Days: {total_days}\n"
        f"- Total Weeks (including partial): {len(weekly_schedule)}\n\n"
    )

    f.write("## Demand\n\n")
    f.write(
        f"- Total Daily Food Demand: {total_daily_food:,.2f} portions\n\n"
    )

    f.write("## Weekly Supplier Schedule\n\n")
    f.write(weekly_schedule.to_markdown(index=False))
    f.write("\n\n")

    f.write("## Assumptions\n\n")
    f.write(
        "- Customer base and insect are assumed constant during the period.\n"
        "- Each row in the master dataset represents one insect.\n"
        "- 'Food portions per day' reflects constant consumption.\n"
        "- Weekly surname-based collection affects timing only, not total demand.\n"
        "- No onboarding or churn is modelled during this period.\n"
    )

    f.write("\n## Operational Interpretation\n\n")
    f.write(
        "Supplier orders must match aggregate biological consumption rather than "
        "customer collection schedule. The final week reflects a partial 3-day period.\n"
    )

print("\nQ3 completed successfully.")
print("Weekly schedule saved.")
