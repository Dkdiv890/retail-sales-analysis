# Retail Sales & Profitability Analytics Portfolio Project

A complete, realistic, and reproducible data analytics portfolio project built using **SQL (SQLite 3)**, **Python (Pandas, Matplotlib, Seaborn)**, and **Microsoft Power BI**.

---

## 1. Project Background & Business Question

Retail businesses frequently focus on top-line sales volume while overlooking margin erosion caused by aggressive promotional discounting, unfavorable product mixes, and regional cost discrepancies.

### Central Business Question:
> **"What are the sales patterns, top-performing categories, and best-performing sub-categories in this retail dataset, and what insights can be derived across customer segments, regions, and discount levels to understand profitability and improve sales performance?"**

---

## 2. Technology Stack

- **Relational Database & SQL:** SQLite 3, indexed tables, CTEs, Window Functions (`DENSE_RANK`, `ROW_NUMBER`, cumulative sums)
- **Programming & Data Wrangling:** Python 3, Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Business Intelligence & Reporting:** Microsoft Power BI (DAX, Star Schema Modeling, Layout Specs)
- **Interactive Analysis:** Jupyter Notebook
- **Spreadsheet Integration:** Excel-compatible summary CSV exports

---

## 3. Project Directory Structure

```
EDA final/
├── data/
│   ├── raw/
│   │   └── SampleSuperstore.csv            # Original raw CSV (13 columns, preserved)
│   ├── cleaned/
│   │   └── Superstore_Cleaned.csv         # Cleaned transaction data (9,977 rows)
│   ├── exports/
│   │   ├── category_summary.csv           # Category KPIs for Excel
│   │   ├── subcategory_summary.csv        # Sub-Category KPIs for Excel
│   │   ├── regional_summary.csv           # Regional & State KPIs for Excel
│   │   ├── segment_summary.csv            # Customer Segment KPIs for Excel
│   │   └── discount_tier_summary.csv      # Discount Band KPIs for Excel
│   └── retail_sales.db                    # SQLite database with indexed tables
├── notebooks/
│   └── retail_sales_analysis.ipynb        # Complete narrative notebook (cleaning, SQL, EDA)
├── src/
│   ├── data_cleaning.py                   # Data inspection, duplicate audit, and cleaning pipeline
│   ├── database_setup.py                  # SQLite schema initialization and data loader
│   ├── run_sql_queries.py                 # Query execution runner logging actual results
│   └── eda_analysis.py                    # Script generating 6 charts and 5 summary CSVs
├── sql/
│   ├── schema.sql                         # Table DDL and analytical index definitions
│   ├── analysis_queries.sql               # 14 structured, commented SQL queries
│   └── query_results.md                   # Actual query outputs and business takeaways
├── visuals/
│   ├── 01_category_sales_profit.png       # Total Sales vs. Net Profit by Category
│   ├── 02_subcategory_profitability.png   # Sub-Category Profit Rankings (Losses in Red)
│   ├── 03_regional_performance.png        # Regional Sales, Profit, and Margin %
│   ├── 04_state_extremes.png              # Top 5 Profitable vs. Bottom 5 Loss States
│   ├── 05_discount_vs_profit_margin.png   # Discount Rate vs. Average Margin %
│   └── 06_segment_and_ship_mode.png       # Customer Segment and Ship Mode distributions
├── reports/
│   ├── data_cleaning_report.md            # Cleaning audit, duplicate rationale, and limits
│   ├── business_findings_report.md        # 5 calculated findings and strategic recommendations
│   └── interview_prep.md                  # Comprehensive interview Q&A and technical guide
├── powerbi/
│   ├── data_model_instructions.md         # Ingestion, data types, and modeling guide
│   ├── dax_measures.dax                   # Verified DAX measures matching SQL/Python parity
│   ├── dashboard_visual_specifications.md # Canvas layout, visual coordinates, and colors
│   └── build_guide.md                     # 15-minute tutorial for Power BI Desktop
├── README.md                              # Project documentation
└── requirements.txt                       # Project dependencies
```

---

## 4. Duplicate Records Investigation & Data Cleaning Audit

Before proceeding with downstream analysis, an in-depth audit of duplicate records was conducted across all 13 columns:
- **Raw Preservation:** 9,994 raw rows preserved unchanged in `data/raw/SampleSuperstore.csv`.
- **Duplicates Identified:** Exactly 17 duplicate rows (34 total rows involved in identical pairs matching 100% across all attributes).
- **Analytical Limitations:** In the absence of an `Order ID` or timestamp, genuine repeated transactions cannot be ruled out conclusively. Removing all 17 exact duplicate rows is not presented as definitively correct or universally industry-standard. However, consecutive identical entries (e.g., identical custom-discounted chairs in Columbus, Ohio) suggest system logging duplication.
- **Deduplication Impact:**
  - **Sales:** $2,297,200.86 -> $2,296,195.59 (-$1,005.27 | -0.0438%)
  - **Profit:** $286,397.02 -> $286,241.42 (-$155.60 | -0.0543%)
  - **Quantity:** 37,873 -> 37,820 units (-53 units | -0.1399%)
  - **Profit Margin:** 12.4672% -> 12.4659% (delta of -0.0013 percentage points)
- **Analytical Decision & Documented Uncertainty:** In the absence of primary keys or timestamps, removing these 17 rows is an explicit analytical modeling assumption rather than an absolute fact or universal standard. It serves as a conservative safeguard against system double-counting while adjusting revenue by only 0.044% and preserving the raw dataset intact (detailed audit log and sensitivity analysis in `reports/data_cleaning_report.md`).

---

## 5. Key Business Findings (Empirically Derived)

Across **9,977 cleaned transaction rows**, the business generated **$2,296,195.59 in sales** and **$286,241.42 in profit** (**12.47% overall profit margin**), with an average transaction value of **$230.15**.

1. **Category Margin Divergence:** Technology delivered **50.8% of total profit** ($145.5k, 17.4% margin) and Office Supplies delivered **42.7%** ($122.4k, 17.0% margin). In contrast, Furniture generated nearly a third of total revenue ($741.3k) but only **6.4% of net profit** ($18.4k, 2.49% margin).
2. **Chronic Loss Centers:** Three sub-categories operated at an aggregate net loss: **Tables (-$17,725.48 net loss)**, **Bookcases (-$3,472.56 net loss)**, and **Supplies (-$1,189.10 net loss)**.
3. **The 20% Discount Drop-Off:** Transactions with 0% discount achieved a **+29.51% profit margin**. When discounts exceeded 20%, average margins turned sharply negative (-19.72%). Transactions with >50% discount generated only $64k in sales while producing **-$76,552.80 in losses**.
4. **Geographic Concentration:** California ($76.3k) and New York ($74.0k) accounted for **over 52% of total profit**. Conversely, Texas (-$25.8k), Ohio (-$17.0k), Pennsylvania (-$15.6k), and Illinois (-$12.6k) suffered severe losses driven by average regional discount rates between 32% and 39%.
5. **Customer Segments & Fulfillment:** The Consumer segment drove 50.55% of revenue and 46.82% of profit. Corporate and Home Office segments maintained resilient margins (13%–14%). Shipping modes all exhibited stable margins (12%–14%), indicating fulfillment pricing is not a source of margin leakage.

---

## 6. SQL Concepts Demonstrated

The 14 executable queries in `sql/analysis_queries.sql` cover:
- **Core Aggregations:** `COUNT(*)`, `SUM()`, `AVG()`, `ROUND()`, `MIN()`, `MAX()`
- **Filtering & Grouping:** `GROUP BY`, `HAVING SUM(profit) < 0`, `WHERE`
- **Conditional Logic:** `CASE WHEN` discount bucketing
- **Common Table Expressions (CTEs):** Modular subqueries for state ranking and summary isolation
- **Window Functions:**
  - `DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC)`
  - `ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(profit) DESC)`
  - `SUM(sales) OVER (ORDER BY sales DESC)` (Cumulative running total / Pareto)
- **Relational JOINs:** Joining derived regional dimension summaries with category sales

All query outputs are logged with tabular results in `sql/query_results.md`.

---

## 7. Mathematical Cross-Validation

Every primary metric was cross-validated between Python (Pandas) and SQL (SQLite 3):
- **Total Transaction Rows:** Python `9,977` | SQL `9,977` | **100% Match**
- **Total Sales:** Python `$2,296,195.59` | SQL `$2,296,195.59` | **100% Match**
- **Total Profit:** Python `$286,241.42` | SQL `$286,241.42` | **100% Match**
- **Overall Margin:** Python `12.47%` | SQL `12.47%` | **100% Match**

---

## 8. How to Reproduce & Run the Project

### Prerequisites:
- Python 3.9+ with `pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`
- SQLite 3 (standard with Python)

### Step-by-Step Commands:
```bash
# 1. Create and activate dedicated virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run data cleaning pipeline (audits duplicates, cleans types, outputs report)
python3 src/data_cleaning.py

# 4. Initialize SQLite database and load cleaned data
python3 src/database_setup.py

# 5. Execute all 14 SQL analytical queries and log results
python3 src/run_sql_queries.py

# 6. Generate publication-quality EDA charts and Excel summary CSVs
python3 src/eda_analysis.py

# 7. Launch the interactive Jupyter Notebook
jupyter notebook notebooks/retail_sales_analysis.ipynb
```

---

## 9. Power BI Dashboard Deliverables Notice

Power BI Desktop is a Windows-native application. To ensure full reproducibility in non-Windows or headless environments, this repository provides:
- Cleaned dataset: `data/cleaned/Superstore_Cleaned.csv`
- Production DAX measures: `powerbi/dax_measures.dax`
- Layout and card visual specifications: `powerbi/dashboard_visual_specifications.md`
- 15-minute assembly tutorial: `powerbi/build_guide.md`

To build the dashboard, launch Power BI Desktop on Windows, load `Superstore_Cleaned.csv`, paste the measures from `dax_measures.dax`, and follow the steps in `build_guide.md`.
