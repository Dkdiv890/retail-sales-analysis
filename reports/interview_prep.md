# Project Interview & Technical Preparation Guide

**Project Title:** Retail Sales & Profitability Analysis using SQL, Python, and Power BI  
**Core Domain:** Retail Analytics, Financial Profitability, Pricing & Discount Governance  

---

## 1. Project Elevator Pitch (30-Second & 2-Minute Versions)

### 30-Second Pitch:
> *"I executed an end-to-end retail sales and profitability analysis on a 10,000-record dataset using Python, SQLite, and Power BI. I cleaned the dataset in Pandas, stored it in an indexed SQLite database, and developed 14 analytical SQL queries utilizing CTEs and window functions. The analysis revealed that 18.7% of transactions operated at a loss, eroding over $156,000 in gross profit. I identified an empirical 20% discount threshold beyond which average margins turn negative, particularly in furniture lines like Tables and Bookcases. I then developed Power BI dashboard specifications and Excel-compatible summary exports to present actionable pricing and margin-recovery recommendations."*

### 2-Minute Deep Dive:
> *"The objective of this project was to analyze how commercial sales patterns, product categories, customer segments, and regional discounting strategies impact bottom-line profitability.
> 
> When auditing the raw dataset, I first identified critical schema boundaries: the dataset contained 13 columns with no date fields or order IDs. Rather than fabricating synthetic dates or confusing individual line items with multi-item orders, I framed a rigorous cross-sectional analysis across categories, sub-categories, geography, and discount bands.
> 
> During data cleaning in Python, I audited 17 identical duplicate records across all 13 fields and documented the justification for removing them to ensure unbiased aggregations. I then ingested the cleaned 9,977 transaction rows into an indexed SQLite relational database.
> 
> In SQL, I authored 14 analytical queries leveraging GROUP BY, HAVING, CTEs, and Window Functions (DENSE_RANK, ROW_NUMBER, and cumulative sums). My findings showed that while Technology and Office Supplies delivered strong 17% profit margins, Furniture yielded just a 2.49% margin despite contributing nearly a third of total revenue. More critically, Tables alone incurred a net loss of $17,725 due to excessive discounting averaging 26%. Furthermore, California and New York generated over 52% of total profit, while four states—Texas, Ohio, Pennsylvania, and Illinois—suffered severe losses driven by regional discount rates exceeding 32%.
> 
> I cross-validated all SQL metrics against Python calculations for 100% mathematical parity, designed 6 Matplotlib/Seaborn visualizations, and authored production DAX measures and layout specifications for Power BI."*

---

## 2. Dataset Schema & Integrity Decisions

| Column | Type | Analytical Treatment & Integrity Decisions |
| :--- | :--- | :--- |
| `Ship Mode` | Categorical | Evaluated across 4 modes; observed stable 12%–14% margins across all classes. |
| `Segment` | Categorical | Consumer, Corporate, Home Office. Consumer accounts for ~50% of volume. |
| `Country` | Categorical | All records represent the United States. |
| `City` & `State` | Categorical | 49 states analyzed; aggregated to isolate regional extremes (Top/Bottom 5). |
| `Postal Code` | Text (VARCHAR) | Cast as zero-padded string rather than numeric to prevent arithmetic operations and preserve leading zeros. |
| `Region` | Categorical | West, East, South, Central. |
| `Category` | Categorical | Furniture, Office Supplies, Technology. |
| `Sub-Category` | Categorical | 17 sub-categories; served as the primary granular product dimension. |
| `Sales` | Decimal | Validated non-negative numeric. |
| `Quantity` | Integer | Validated positive integers (1 to 14 units). |
| `Discount` | Decimal (Rate) | Bounded rate [0.0 to 0.8]; used to evaluate margin erosion. |
| `Profit` | Decimal | Signed numeric; retained negative values to identify loss-making transactions. |

---

## 3. Explaining Technical SQL Concepts Used

### A. GROUP BY & HAVING
- **What it does:** Groups raw rows by categorical dimensions and applies aggregate functions (`SUM`, `AVG`, `COUNT`).
- **Where we used it:** 
  - `GROUP BY category, sub_category` to calculate total revenue, profit, and average discount.
  - `HAVING SUM(profit) < 0` to filter only the 3 sub-categories that operated at a net aggregate loss (Tables, Bookcases, Supplies).
- **Key Difference:** `WHERE` filters individual rows before aggregation; `HAVING` filters aggregated groups after the `GROUP BY` calculation is completed.

### B. Common Table Expressions (CTEs)
- **What it does:** Defines a named temporary result set (`WITH cte_name AS (...)`) that improves query readability and modularity compared to nested subqueries.
- **Where we used it:** 
  - Query 6 (State Extremes): Created `state_profitability` CTE, then queried `top_5_states` and `bottom_5_states`, combining them with `UNION ALL`.
  - Query 12 (Top State Per Region): Used a CTE to compute regional state rankings before filtering for the top rank.

### C. Window Functions: DENSE_RANK vs. ROW_NUMBER vs. Running Totals
- **`DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC)`**
  - Ranks sub-categories within their parent category without skipping ranks if there are ties.
- **`ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(profit) DESC)`**
  - Assigns a unique sequential integer (1, 2, 3...) to states within each region, allowing clean filtering with `WHERE rank_in_region = 1` to isolate the top-performing state per region.
- **`SUM(sales) OVER (ORDER BY sales DESC)`**
  - Computes a cumulative running total across sub-categories for Pareto distribution analysis.

---

## 4. Key Performance Indicators (KPIs)

- **Total Transactions:** `COUNT(*)` = **9,977** (Explicitly labeled as transaction rows, not orders).
- **Total Sales:** `SUM(sales)` = **$2,296,195.59**.
- **Total Profit:** `SUM(profit)` = **$286,241.42**.
- **Profit Margin %:** `SUM(profit) / SUM(sales) * 100` = **12.47%**.
- **Average Sales Per Transaction:** `$2,296,195.59 / 9,977` = **$230.15**.
- **Loss-Making Transactions:** `COUNT(*) WHERE profit < 0` = **1,869** (18.73% of all transactions).
- **Total Loss Amount:** `SUM(profit) WHERE profit < 0` = **-$156,112.99**.

---

## 5. Top 10 Technical & Analytical Interview Questions

### Q1: Why did you remove the 17 duplicate records?
> *"When auditing the dataset, I found 17 records with 100% identical values across all 13 columns—including exact fractional sales and profit numbers down to four decimal places. Because this dataset lacks unique order IDs or timestamps, these identical records represent duplicate data entry rather than independent transactions. Leaving them in would artificially inflate transaction counts and skew sales aggregates. I documented this explicitly in the cleaning report before dropping them."*

### Q2: Why did you not analyze monthly or seasonal sales trends?
> *"A fundamental responsibility of a data analyst is respecting data integrity. The provided `SampleSuperstore.csv` contains 13 columns and does not have an `Order Date` or `Ship Date`. Rather than fabricating synthetic dates or silently swapping the dataset, I honestly documented this limitation and pivoted to deep cross-sectional analysis across categories, sub-categories, geography, and discount bands."*

### Q3: Why do you distinguish 'Transaction Rows' from 'Orders'?
> *"In relational retail databases, a single customer order often contains multiple line items. Because this dataset lacks an `Order ID` column, treating each row as a distinct order would be an unverified assumption. Calling them 'Transaction Rows' or 'Line Items' is factually accurate, prevents misleading stakeholders on order frequency, and avoids invalid metrics like Average Order Value."*

### Q4: What is the most critical business insight you discovered?
> *"The discovery of the 20% discount threshold and category margin divergence. Transactions with zero discount generated a 29.5% profit margin. But once discounts exceed 20%, average profits turn negative. The >50% discount tier generated only $64k in sales but incurred over $76k in losses. This was especially damaging in Furniture, where Tables generated $206k in sales but suffered a net loss of $17.7k due to a 26% average discount rate."*

### Q5: How did you ensure your Python EDA and SQL queries were accurate?
> *"I built an automated cross-validation step in Python where I queried the SQLite database and compared `COUNT(*)`, `SUM(sales)`, and `SUM(profit)` against Pandas dataframe calculations. Both engines produced exact matches ($2,296,195.59 in sales and $286,241.42 in profit), guaranteeing 100% mathematical parity across deliverables."*

### Q6: Can you explain how you used Window Functions in this project?
> *"I used window functions in three distinct queries: 
> First, `DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC)` to rank sub-categories within their respective categories. 
> Second, `ROW_NUMBER() OVER (PARTITION BY region ORDER BY profit DESC)` inside a CTE to isolate the single highest-profit state in each region. 
> Third, `SUM(sales) OVER (ORDER BY sales DESC)` to compute running sales totals for Pareto cumulative percentage analysis."*

### Q7: If leadership says 'Discounts increase sales volume, so we should keep discounting,' how would you respond?
> *"I would present the empirical data: while low discounts (1–20%) generate positive profits ($100k profit on $846k sales), transactions discounted above 50% produced only $64k in revenue while generating $76k in net losses. High-volume discounting is eroding more margin than it creates in gross volume, particularly in states like Texas and Illinois where average discounts exceed 37% and overall state profits are deeply negative."*

### Q8: What recommendations would you give to executive leadership?
> *"Three immediate, practical steps:
> 1. **Discount Governance:** Implement an approval workflow for any discount above 20%, and eliminate promotional discounts above 50% except for dead inventory liquidation.
> 2. **Product Margin Restructuring:** Cap discounting on Tables and Bookcases, and explore product bundling with high-margin items like Accessories or Office Supplies.
> 3. **Regional Sales Incentive Realignment:** In Central states (Texas, Illinois) and East-Central states (Ohio, Pennsylvania), shift regional sales commission from gross sales volume to gross margin dollars."*

### Q9: How would you describe your Power BI dashboard architecture?
> *"I structured the dashboard with a clean visual hierarchy: 5 executive KPI cards across the top banner, followed by category comparison and conditional-formatted sub-category bar charts. I authored 10 dedicated DAX measures in a centralized `_Measures` table, including dynamic color formatting measures (`SubCategory Profit Color`) to automatically highlight loss-making sub-categories in red. I also added multi-select slicers for Region, Category, Segment, and Ship Mode."*

### Q10: What are the limitations of this analysis?
> *"First, correlation is not causation—we observe that high discounts coincide with heavy losses, but we cannot measure competitor actions or store traffic without experimental data. Second, without customer IDs or timestamps, we cannot evaluate customer lifetime value (LTV), repeat purchase rates, or seasonal trends."*
