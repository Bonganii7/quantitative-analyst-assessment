# Quantitative Analyst Assessment  
**Name:** Bongani  

---

## Overview

This repository contains my completed assessment for the Quantitative Analyst role.

The objective was to analyse customer and operational data for a pet store and provide:

1. A high-level overview of the store and customer base  
2. A weekly food calculation for an individual customer  
3. A weekly supplier ordering schedule  
4. A two-year sales forecast with documented assumptions and risk factors  

All results are reproducible and generated via Python scripts.

---

## Project Structure

```
quant/
│
├── data/                 # Cleaned master dataset
├── docs/                 # Generated reports and visualisations
│   ├── question_1/
│   ├── question_2/
│   ├── question_3/
│   ├── question_4/
│   ├── data_integrity_report.md
│   └── methodology.md
│
├── src/                  # Analytical scripts
│   ├── Q1_overview.py
│   ├── Q2_msgraden.py
│   ├── Q3_weekly_foodneed.py
│   ├── Q4_forecast.py
│
├── README.md
└── requirements.txt
```

All final outputs are available in the `/docs` directory for direct review.

---

## Question Summary

### Question 1 – Store Overview
- Customer base size and segmentation  
- Insect ownership distribution  
- Store scale analysis  
- Data integrity validation  

### Question 2 – Weekly Food Order (Individual)
- Customer-level filtering  
- Insect count and terrarium ownership  
- Daily and weekly food requirement calculation  
- Explicit structural assumptions documented  

### Question 3 – Weekly Supplier Ordering
- Total store daily food demand  
- Week-by-week schedule (Apr 1 – Aug 1 2020)  
- Partial final week handled explicitly (17 full weeks + 3 days)  
- Operational interpretation provided  

### Question 4 – Two-Year Sales Forecast
- Reconstructed monthly active customers from purchase data  
- Linear regression fitted to cumulative growth  
- 24-month forward projection  
- Scenario bands based on regression uncertainty  
- Translation from customers → food demand  
- Internal drivers and external risk factors documented  

---

## Forecasting Approach (Q4)

The model assumes:

- Linear continuation of historical customer growth  
- No churn explicitly modelled  
- Stable average food demand per customer  
- No structural shift in ownership behaviour  

Scenario bands are derived using:

`slope ± 1.96 × standard error`

External economic and regulatory factors are acknowledged as potential risks but are not explicitly modelled.

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scripts:

```bash
python src/Q1_overview.py
python src/Q2_msgraden.py
python src/Q3_weekly_foodneed.py
python src/Q4_forecast.py
```

Outputs will be saved in the `/docs` directory.

---

Thank you for reviewing this assessment.
