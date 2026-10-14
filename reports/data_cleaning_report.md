# Data Cleaning & Integrity Report: Retail Sales Dataset

## 1. Executive Summary
- **Initial Raw Records:** 9,994 rows across 13 columns
- **Duplicates Identified:** 17 duplicate records
- **Final Cleaned Records:** 9,977 transaction rows
- **Total Missing Values:** 0 nulls detected across all columns

## 2. Missing Value Audit
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

## 3. Duplicate Records Investigation
- **Audit Finding:** 17 rows had 100% identical values across all 13 attributes.
- **Sample Duplicate Records (Inspected):**

| Ship Mode      | Segment     | City          | State      | Category        | Sub-Category   |   Sales |   Profit |
|:---------------|:------------|:--------------|:-----------|:----------------|:---------------|--------:|---------:|
| Standard Class | Consumer    | Los Angeles   | California | Office Supplies | Paper          |   19.44 |   9.3312 |
| Standard Class | Consumer    | Los Angeles   | California | Office Supplies | Paper          |   19.44 |   9.3312 |
| Standard Class | Corporate   | San Francisco | California | Office Supplies | Art            |   11.76 |   3.1752 |
| Standard Class | Corporate   | San Francisco | California | Office Supplies | Art            |   11.76 |   3.1752 |
| Same Day       | Home Office | San Francisco | California | Office Supplies | Labels         |   41.4  |  19.872  |

- **Action & Rationale:** In the absence of unique transaction/order timestamps or IDs, identical records matching across all dimension values, exact unit quantities, and exact fractional sales/profit figures indicate data ingestion duplication. These 17 duplicate rows were removed, retaining the first occurrence to ensure unbiased aggregate calculations.

## 4. Column Transformation & Data Type Corrections
| Column | Original Type | Target Type | Cleaning Transformation |
| :--- | :--- | :--- | :--- |
| `Postal Code` | Numeric (int64/float64) | String (VARCHAR) | Converted to string with zero-padding; prevents arithmetic misuse |
| Text Columns (8) | Object | String | Stripped leading/trailing whitespace |
| `Sales` | Float64 | Float64 (Numeric) | Validated non-negative numeric |
| `Quantity` | Int64 | Integer | Validated positive integer |
| `Discount` | Float64 | Float64 (Rate) | Validated bounded rate [0.0, 1.0] |
| `Profit` | Float64 | Float64 (Numeric) | Retained signed numeric (supports losses) |
| `Profit_Margin` | *None* | Float64 (Derived) | Calculated as `Profit / Sales` (rounded to 4 decimal places) |
| `Discount_Tier` | *None* | Categorical (Derived) | Binned into `0%`, `1-20%`, `21-50%`, and `>50%` |

## 5. Summary Statistics of Cleaned Dataset

|               |   count |     mean |      std |       min |     25% |    50% |      75% |      max |
|:--------------|--------:|---------:|---------:|----------:|--------:|-------:|---------:|---------:|
| Sales         |    9977 | 230.149  | 623.721  |     0.444 | 17.3    | 54.816 | 209.97   | 22638.5  |
| Quantity      |    9977 |   3.7907 |   2.2267 |     1     |  2      |  3     |   5      |    14    |
| Discount      |    9977 |   0.1563 |   0.2065 |     0     |  0      |  0.2   |   0.2    |     0.8  |
| Profit        |    9977 |  28.6901 | 234.458  | -6599.98  |  1.7262 |  8.671 |  29.372  |  8399.98 |
| Profit_Margin |    9977 |   0.1201 |   0.4666 |    -2.75  |  0.075  |  0.27  |   0.3625 |     0.5  |

## 6. Documented Data Constraints & Limitations
1. **Absence of Temporal Dimensions:** No `Order Date` or `Ship Date` columns exist. Longitudinal and seasonal analyses are not feasible on this dataset.
2. **Transaction-Row Granularity:** No `Order ID` is present. Metrics are computed at the transaction-row level (total transactions, average sales per transaction) rather than aggregated order-level metrics.
3. **Product Hierarchy:** No `Product ID` or `Product Name` is available. Granular product analysis is bounded to the 17 `Sub-Category` groupings.
