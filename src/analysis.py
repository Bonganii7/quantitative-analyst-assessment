"""
Data Integrity & Master Dataset Build


Stage 1: I validate, do some cleaning & build master

Version 1 is raq dimension, where duplicate keys retained. And version 1 is the cleaned dimension (duplicates resolved)
"""

import pandas as pd



file_path = r"..\data\Quant_Questions (1).xlsx"


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


#load data

section("Loading Data")

insects = pd.read_excel(file_path, sheet_name="Insects")
customers = pd.read_excel(file_path, sheet_name="Customers")
terrarium = pd.read_excel(file_path, sheet_name="Terrarium")
population = pd.read_excel(file_path, sheet_name="Population")

print("Insects:", insects.shape)
print("Customers:", customers.shape)
print("Terrarium:", terrarium.shape)
print("Population:", population.shape)


# validate fields
section("Field-Level Null Check")

print("Insects\n", insects.isnull().sum())
print("Customers\n", customers.isnull().sum())
print("Terrarium\n", terrarium.isnull().sum())
print("Population\n", population.isnull().sum())


#validate now the data integrity
section("Foreign Key Validation")

missing_terrariums = set(population["Terrarium"]) - set(terrarium["Name"])
missing_customers = set(terrarium["customer identifier"]) - set(customers["cust_no"])
missing_insects = set(population["insect"]) - set(insects["key"])

print(f"Missing Terrariums: {len(missing_terrariums)}")
print(f"Missing Customers: {len(missing_customers)}")
print("Missing Insects:", missing_insects)

affected_rows = population[population["insect"].isin(missing_insects)]
print("Affected Rows (Missing Insects):", affected_rows.shape[0])

section("Check if tpe matches insect keys")
invalid_tpe = set(customers["tpe"]) - set(insects["key"])
print("Invalid tpe values:", invalid_tpe)

print("Confirmind 'd' not here: ", sorted(insects["key"].unique()))


#insect dimension and analysis
section("Insect Dimension Distribution")

print(insects["food portions per day"].describe())
print("\nValue Counts:\n")
print(insects["food portions per day"].value_counts())

section("Duplicate Insect Keys (Raw Dimension)")

duplicate_keys = insects[insects.duplicated("key", keep=False)]
print(duplicate_keys.sort_values("key"))


# V1- verision 1 master build with duplicates
"""
V1 MASTER BUILD

Issues:
- Duplicate insect keys exist ('m', 'x')
- Merge will cause row inflation (fan-out join)
- This version retained only to document
"""

section("V1 - Imputing Missing Insect 'd'")

median_food = insects["food portions per day"].median()

insects_corrected_v1 = pd.concat([
    insects,
    pd.DataFrame({
        "key": ["d"],
        "description": ["Unknown insect type (imputed)"],
        "food portions per day": [median_food]
    })
], ignore_index=True)

print("V1 Insect Rows:", insects_corrected_v1.shape[0])

section("Building Master Dataset - V1")

master_v1 = population.merge(
    terrarium,
    left_on="Terrarium",
    right_on="Name",
    how="left"
)

master_v1 = master_v1.merge(
    customers,
    left_on="customer identifier",
    right_on="cust_no",
    how="left"
)

master_v1 = master_v1.merge(
    insects_corrected_v1,
    left_on="insect",
    right_on="key",
    how="left"
)

print("Master Shape (V1):", master_v1.shape)


#V2 - version 2 clean insect dimension

section("V2 - Resolving Duplicate Insect Keys")

insects_clean_v2 = (
    insects
    .groupby("key", as_index=False)
    .agg({
        "description": "first",
        "food portions per day": "median"
    })
)

print("Original rows:", insects.shape[0])
print("After collapsing duplicates:", insects_clean_v2.shape[0])
print("Unique keys:", insects_clean_v2["key"].nunique())


section("V2 - Imputing Missing Insect 'd'")

median_food_v2 = insects_clean_v2["food portions per day"].median()

insects_corrected_v2 = pd.concat([
    insects_clean_v2,
    pd.DataFrame({
        "key": ["d"],
        "description": ["Unknown insect type (imputed)"],
        "food portions per day": [median_food_v2]
    })
], ignore_index=True)

print("Final insect rows (V2):", insects_corrected_v2.shape[0])
print("Final unique keys (V2):", insects_corrected_v2["key"].nunique())



#V2 – MASTER BUILD final
# ============================================================

section("Building Master Dataset - V2")

master_v2 = population.merge(
    terrarium,
    left_on="Terrarium",
    right_on="Name",
    how="left"
)

master_v2 = master_v2.merge(
    customers,
    left_on="customer identifier",
    right_on="cust_no",
    how="left"
)

master_v2 = master_v2.merge(
    insects_corrected_v2,
    left_on="insect",
    right_on="key",
    how="left"
)

print("Master Shape (V2):", master_v2.shape)

section("Post-Merge Null Check (V2)")
print(master_v2.isnull().sum())



#8 V1 vs V2 – ROW INFLATION COMPARISON
# ============================================================

section("Row Inflation Comparison")

print("Population rows :", population.shape[0])
print("Master V1 rows  :", master_v1.shape[0])
print("Master V2 rows  :", master_v2.shape[0])

print("Inflation caused by duplicate keys:",
      master_v1.shape[0] - master_v2.shape[0])

# Save clean master dataset
master_v2.to_csv("../data/master_clean.csv", index=False)

print("\nClean master dataset saved to /data/master_clean.csv")
