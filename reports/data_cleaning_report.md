# Data Cleaning & Integrity Report: Retail Sales Dataset

## 1. Executive Summary
- **Initial Raw Records:** 9,994 rows across 13 columns
- **Identified Duplicate Records:** 17 duplicate records (34 rows involved in identical pairs)
- **Final Cleaned Records:** 9,977 transaction rows
- **Total Missing Values:** 0 nulls detected across all 13 columns
- **Sales Impact of Deduplication:** -$1,005.27 (0.0438% of total revenue)
- **Profit Impact of Deduplication:** -$155.60 (0.0543% of total net profit)
- **Margin Impact:** 12.4672% -> 12.4659% (delta of -0.0013 percentage points)

---

## 2. In-Depth Duplicate Records Investigation

### A. Audit Findings
A full-table audit across all 13 columns identified exactly **17 duplicate rows** (17 primary occurrences + 17 duplicate repeats = 34 total rows affected).

### B. Complete Log of Inspected Duplicate Pairs
| Index | Ship Mode | Segment | City | State | Category | Sub-Category | Sales | Qty | Discount | Profit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2836 / 4117 | Standard Class | Consumer | Los Angeles | California | Office Supplies | Paper | $19.44 | 3 | 0.0 | $9.3312 |
| 3412 / 6146 | Standard Class | Corporate | San Francisco | California | Office Supplies | Art | $11.76 | 4 | 0.0 | $3.1752 |
| 5493 / 5905 | Same Day | Home Office | San Francisco | California | Office Supplies | Labels | $41.40 | 4 | 0.0 | $19.8720 |
| 2803 / 4553 | Standard Class | Consumer | San Francisco | California | Office Supplies | Paper | $12.84 | 3 | 0.0 | $5.7780 |
| 1479 / 7608 | Standard Class | Consumer | San Francisco | California | Office Supplies | Paper | $25.92 | 4 | 0.0 | $12.4416 |
| 8457 / 9477 | Second Class | Corporate | Chicago | Illinois | Office Supplies | Binders | $3.56 | 3 | 0.8 | $-6.2370 |
| 8533 / 9262 | Standard Class | Consumer | Detroit | Michigan | Furniture | Chairs | $389.97 | 3 | 0.0 | $35.0973 |
| 3127 / 6334 | Standard Class | Consumer | New York City | New York | Office Supplies | Paper | $49.12 | 4 | 0.0 | $23.0864 |
| 3405 / 3406 | Standard Class | Home Office | Columbus | Ohio | Furniture | Chairs | $281.37 | 2 | 0.3 | $-12.0588 |
| 591 / 3670 | Standard Class | Consumer | Salem | Oregon | Office Supplies | Paper | $10.37 | 2 | 0.2 | $3.6288 |
| 935 / 950 | Standard Class | Home Office | Philadelphia | Pennsylvania | Office Supplies | Paper | $15.55 | 3 | 0.2 | $5.4432 |
| 5372 / 7759 | Standard Class | Corporate | Houston | Texas | Office Supplies | Paper | $15.55 | 3 | 0.2 | $5.4432 |
| 6409 / 8032 | First Class | Consumer | Houston | Texas | Office Supplies | Paper | $47.95 | 3 | 0.2 | $16.1838 |
| 6245 / 9363 | Standard Class | Home Office | Seattle | Washington | Furniture | Furnishings | $22.14 | 3 | 0.0 | $6.4206 |
| 2807 / 8095 | Second Class | Consumer | Seattle | Washington | Office Supplies | Paper | $12.96 | 2 | 0.0 | $6.2208 |
| 568 / 7735 | Standard Class | Corporate | Seattle | Washington | Office Supplies | Paper | $19.44 | 3 | 0.0 | $9.3312 |
| 1186 / 6357 | Standard Class | Corporate | Seattle | Washington | Office Supplies | Paper | $25.92 | 4 | 0.0 | $12.4416 |

### C. Analytical Limitations of Evaluating Duplicates in this Dataset
1. **Absence of Unique Primary Keys:** Without an `Order ID` or `Transaction ID`, it is impossible to definitively determine if two identical rows represent a single transaction recorded twice or two genuine separate customer transactions.
2. **Absence of Timestamps:** Without `Order Date` or `Time`, we cannot evaluate whether identical purchases occurred at the exact same second (indicating a technical re-try/duplicate entry) or months apart across different shopping cycles.
3. **Evidence of Ingestion Duplication:** Rows 3405 and 3406 are consecutive rows in the dataset featuring identical custom discounts (30%) and exact fractional negative profit (`-$12.0588`) on Chairs in Columbus, Ohio. Such consecutive identical entries strongly suggest duplicate system logging.

### D. Quantitative Impact: Before vs. After Deduplication

| Metric | Before Deduplication (Raw) | After Deduplication (Cleaned) | Absolute Delta | Percentage Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Row Count** | 9,994 rows | 9,977 rows | -17 rows | -0.1701% |
| **Total Sales** | $2,297,200.86 | $2,296,195.59 | -$1,005.27 | -0.0438% |
| **Total Profit** | $286,397.02 | $286,241.42 | -$155.60 | -0.0543% |
| **Total Quantity** | 37,873 units | 37,820 units | -53 units | -0.1399% |
| **Profit Margin** | 12.4672% | 12.4659% | -0.0013% | Minimal (-0.01 bps) |

### E. Analytical Modeling Decision & Documented Uncertainty
- **Documented Decision:** Deduplicate to 9,977 rows by retaining the first occurrence of identical entries.
- **Methodological Context & Inherent Uncertainty:**
  1. **Analytical Assumption, Not Absolute Fact:** Because the dataset lacks unique transaction keys (`Order ID`) and temporal stamps (`Order Date`, `Time`), genuine repeated purchases cannot be ruled out conclusively. Removing all 17 exact duplicate rows is therefore NOT presented as definitively correct or universally industry-standard, but rather as an explicit analytical assumption.
  2. **Conservative Double-Counting Prevention:** Deduplication was chosen as a conservative baseline to guard against potential technical re-entries or batch ingestion repeats (as evidenced by consecutive identical pairs like rows 3405 and 3406).
  3. **Materiality & Sensitivity:** As shown in the comparison table above, removing these 17 rows changes total revenue by only 0.0438% and overall margin by -0.0013 percentage points. Consequently, whether an analyst chooses to retain all 9,994 rows or deduplicate to 9,977 rows, the commercial findings, category dynamics, and strategic takeaways remain virtually identical.
  4. **Preservation of Raw Baseline:** The original 9,994-row raw dataset is preserved unchanged at `data/raw/SampleSuperstore.csv` and root `SampleSuperstore.csv` to ensure complete auditability, reproducibility, and flexibility for alternative modeling assumptions.

---

## 3. Missing Value Audit
| Column Name | Null Count | Null % | Action Taken |
| :--- | :--- | :--- | :--- |
| `Ship Mode` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Segment` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Country` | 0 | 0.00% | Validated complete (No imputation needed) |
| `City` | 0 | 0.00% | Validated complete (No imputation needed) |
| `State` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Postal Code` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Region` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Category` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Sub-Category` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Sales` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Quantity` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Discount` | 0 | 0.00% | Validated complete (No imputation needed) |
| `Profit` | 0 | 0.00% | Validated complete (No imputation needed) |

---

## 4. Column Transformations & Data Types
| Column | Original Type | Cleaned Type | Cleaning Transformation |
| :--- | :--- | :--- | :--- |
| `Postal Code` | Numeric (int64/float64) | String (VARCHAR) | Cast as zero-padded 5-digit string; prevents numeric arithmetic |
| Text Columns (8) | Object | String | Stripped whitespace and normalized casing |
| `Sales` | Float64 | Float64 | Validated non-negative numeric |
| `Quantity` | Int64 | Integer | Validated positive integers |
| `Discount` | Float64 | Float64 | Validated bounded rate [0.0, 1.0] |
| `Profit` | Float64 | Float64 | Retained signed numeric (supports negative losses) |
| `Profit_Margin` | *None* | Float64 (Derived) | Calculated as `ROUND(Profit / Sales, 4)` |
| `Discount_Tier` | *None* | Categorical (Derived)| Binned into `0%`, `1-20%`, `21-50%`, and `>50%` |

---

## 5. Summary Statistics of Cleaned Dataset

| Metric | count | mean | std | min | 25% | 50% | 75% | max |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Sales** | 9,977 | 230.15 | 623.72 | 0.44 | 17.30 | 54.82 | 209.97 | 22,638.48 |
| **Quantity** | 9,977 | 3.79 | 2.23 | 1.00 | 2.00 | 3.00 | 5.00 | 14.00 |
| **Discount** | 9,977 | 0.16 | 0.21 | 0.00 | 0.00 | 0.20 | 0.20 | 0.80 |
| **Profit** | 9,977 | 28.69 | 234.46 | -6,599.98 | 1.73 | 8.67 | 29.37 | 8,399.98 |
| **Profit_Margin** | 9,977 | 0.12 | 0.47 | -2.75 | 0.07 | 0.27 | 0.36 | 0.50 |

---

## 6. Documented Data Constraints & Scope Boundaries
1. **Absence of Temporal Dimensions:** No `Order Date` or `Ship Date` exists; time-series analysis is excluded.
2. **Transaction-Row Granularity:** No `Order ID` exists; all counts reflect transaction rows.
3. **Product Hierarchy:** No `Product ID` or `Product Name` exists; analysis is bounded to 17 `Sub-Categories`.
