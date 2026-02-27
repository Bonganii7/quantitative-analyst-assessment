"""
Question 1 – High-Level Store & Customer Overview

"""

import pandas as pd
import matplotlib.pyplot as plt
import os



DATA_PATH = "../data/master_clean.csv"
DOCS_OUTPUT_PATH = "../docs/question_1/"

os.makedirs(DOCS_OUTPUT_PATH, exist_ok=True)


# load data

master = pd.read_csv(DATA_PATH)



# STORE METRICS
# ============================================================

active_customers = master["cust_no"].nunique()
active_terrariums = master["Terrarium"].nunique()
total_insects = master.shape[0]
unique_species = master["key"].nunique()
total_food_per_day = master["food portions per day"].sum()

avg_insects_per_terrarium = total_insects / active_terrariums
avg_food_per_terrarium = total_food_per_day / active_terrariums



# CUSTOMER METRICS
# ============================================================

customer_stats = (
    master.groupby("cust_no")
    .agg(
        insect_count=("insect", "count"),
        terrarium_count=("Terrarium", "nunique")
    )
)

avg_terrariums_per_customer = customer_stats["terrarium_count"].mean()
avg_insects_per_customer = customer_stats["insect_count"].mean()


# segmenting the customer now
small = (customer_stats["insect_count"] <= 10).sum()
medium = ((customer_stats["insect_count"] > 10) &
          (customer_stats["insect_count"] <= 30)).sum()
large = (customer_stats["insect_count"] > 30).sum()


#visulisation for store

plt.figure(figsize=(6,5))

labels = ["Customers", "Terrariums", "Insects"]
values = [active_customers, active_terrariums, total_insects]

bars = plt.bar(labels, values,
               color=["#2E86C1", "#28B463", "#F39C12"])

plt.title("Pet Store Overview")
plt.ylabel("Count")

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f"{int(height)}",
             ha="center",
             va="bottom")

plt.tight_layout()
plt.savefig(DOCS_OUTPUT_PATH + "q1_store_scale.png")
plt.close()

# vis customer overview

plt.figure(figsize=(7,5))

labels = ["Small (1–10 insects)",
          "Medium (11–30 insects)",
          "Large (30+ insects)"]

values = [small, medium, large]
total_customers = small + medium + large

bars = plt.bar(labels, values,
               color=["#5DADE2", "#AF7AC5", "#E74C3C"])

plt.title("Customer Segmentation by Insect Ownership", fontsize=12)
plt.xlabel("Customer Size Segment")
plt.ylabel("Number of Customers")

# Add data labels (count + percentage)

for bar in bars:
    height = bar.get_height()
    percentage = (height / total_customers) * 100

    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f"{int(height)} ({percentage:.1f}%)",
             ha="center",
             va="bottom")

plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(DOCS_OUTPUT_PATH + "q1_customer_segments.png")
plt.close()


# see question 1 report

with open(DOCS_OUTPUT_PATH + "q1_report.md", "w") as f:

    f.write("# Question 1 High-Level Store & Customer Overview\n\n")

    # ---------------- Store Overview ----------------
    f.write("## Store Overview\n\n")
    f.write(
        f"- Active Customers: {active_customers}\n"
        f"- Active Terrariums: {active_terrariums}\n"
        f"- Total Insects: {total_insects}\n"
        f"- Unique Species: {unique_species}\n"
        f"- Total Daily Food Demand: {round(total_food_per_day,1)} portions\n"
        f"- Avg Insects per Terrarium: {round(avg_insects_per_terrarium,2)}\n"
        f"- Avg Food per Terrarium per Day: {round(avg_food_per_terrarium,2)}\n\n"
    )

    # ---------------- Customer Overview ----------------
    f.write("## Customer Overview\n\n")
    f.write(
        f"- Avg Terrariums per Customer: {round(avg_terrariums_per_customer,2)}\n"
        f"- Avg Insects per Customer: {round(avg_insects_per_customer,2)}\n"
        f"- Small Owners (1–10 insects): {small}\n"
        f"- Medium Owners (11–30 insects): {medium}\n"
        f"- Large Owners (30+ insects): {large}\n\n"
    )

    # ---------------- Assessment ----------------
    f.write("## Assessment on Question 1\n\n")
    f.write(
        "The store has just under 200 active customers managing almost 600 terrariums. "
        "On average, each terrarium holds about 9 insects, which suggests the overall density "
        "is reasonable and operationally manageable.\n\n"
        "Most customers sit in the medium ownership range (11–30 insects), meaning the store "
        "mainly serves regular hobbyists rather than one-time or very small buyers. At the same "
        "time, the 64 larger owners are important, as they are likely responsible for a significant "
        "portion of the total food demand.\n\n"
        "Overall, the business structure looks steady, with consistent daily feeding requirements "
        "and a fairly balanced mix of small, medium and large customers.\n"
    )

print("\nQ1 report generated successfully.")
