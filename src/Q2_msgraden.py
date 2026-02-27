"""
Question 2 Ms. Graden Weekly Food Order

"""

import pandas as pd
import os

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "../data/master_clean.csv"
DOCS_OUTPUT_PATH = "../docs/question_2/"
os.makedirs(DOCS_OUTPUT_PATH, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

master = pd.read_csv(DATA_PATH)

# ============================================================
# FILTER MS. GRADEN
# ============================================================


ms_graden = master[master["Name_y"].str.contains("Graden", case=False)]

# Safety check
if ms_graden.empty:
   raise ValueError("Ms. Graden not found in dataset.")

"""
ms_graden = master[master["cust_no"] == 283]

if ms_graden.empty:
    raise ValueError("Ms. Graden not found in dataset.")
    
"""

# ============================================================
# CALCULATE METRICS
# ============================================================

total_insects = ms_graden.shape[0]
total_terrariums = ms_graden["Terrarium"].nunique()

daily_food = ms_graden["food portions per day"].sum()
weekly_food = daily_food * 7

# ============================================================
# REPORT
# ============================================================

with open(DOCS_OUTPUT_PATH + "q2_report.md", "w") as f:
    f.write("# Question 2 Ms. Graden Weekly Food Order\n\n")

    f.write("## Customer Details\n\n")
    f.write(
        f"- Customer: Ms Graden\n"
        f"- Total Terrariums Owned: {total_terrariums}\n"
        f"- Total Insects Owned: {total_insects}\n\n"
    )

    f.write("## Food Calculation\n\n")
    f.write(
        f"- Total Daily Food Requirement: {round(daily_food,2)} portions\n"
        f"- Weekly Food Requirement (7days): {round(weekly_food,2)} portions\n"
    )

print("\nQ2 completed successfully.")
print("Weekly Food Ordered:", round(weekly_food,2))
