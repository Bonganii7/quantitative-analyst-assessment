# Quant Assessment – My Processes and Approach  
## Data Integrity Validation & Master Dataset Construction  

---

# 1. Objective

Before doing any analytical work, the aim was to start by reviewing the raw data structure and validated to ensure relational integrity and prevent aggregation errors caused by dimension inconsistencies.

Two master dataset: 
- V1 – Raw insect dimension (with duplicates )
- V2 – Cleaned insect dimension (duplicates resolved)

---

# 2. Dataset Overview

| Table      | Rows | Columns |
|------------|------|---------|
| Insects    | 27   | 3 |
| Customers  | 200  | 5 |
| Terrarium  | 600  | 3 |
| Population | 5,216| 2 |

The **Population** table represents the fact table (insect instances per terrarium).

---

# 3. Field-Level Validation

- No null values were found in any table.
- All primary key fields were complete.
- No structural missing data detected.

---

# 4. Relational Integrity Checks

Foreign key validation results:

- Missing Terrariums: **0**
- Missing Customers: **0**
- Missing Insects: **{'d'}**
- Affected population rows: **189**

### Issue Identified

The insect key `'d'` exists in the **Population** table but does not exist in the **Insects** dimension table.

This creates a referential integrity break and would result in missing dimension data during joins.

---

# 5. Insect Dimension Issues Identified

## Duplicate Primary Keys

The insect dimension contains duplicate keys:

| Key | Description  | Food Portions per Day |
|-----|-------------|-----------------------|
| m   | Maggot      | 7 |
| m   | Mango       | 4 |
| x   | Xigua       | 1 |
| x   | Xylodromus  | 8 |

This violates primary key uniqueness.

Th above causes a **fan-out join**, andd inflates fact rows during master dataset construction.

---

# 6. V1 – Raw Master Build (With Duplicate Keys)

Duplicates retained intentionally to measure impact.

| Metric | Value |
|--------|-------|
| Population rows | 5,216 |
| Master V1 rows  | 5,615 |
| Row inflation   | +399 |

### Observation

Duplicate dimension keys caused 399 additional rows due to fan-out joins.

I only kept V1 for documentation and for comparison purposes.

---

# V2 – Clean Master Build 

### Steps Taken

1. Duplicate insect keys collapsed using **median food value**.
2. Missing insect `'d'` imputed using median food value.
3. Dimension rebuilt with unique keys.
4. Master dataset reconstructed.

### Results

| Metric | Value |
|--------|-------|
| Population rows | 5,216 |
| Master V2 rows  | 5,216 |
| Row inflation   | 0 |

All foreign keys successfully resolved.

No post-merge null values detected.

---

#  Database 

Clean master dataset saved to:
/data/master_clean.csv