# SQL Analytical Query Execution & Results Log

Database: `data/retail_sales.db` (SQLite 3) | Source Table: `superstore_sales` (9,977 Cleaned Transaction Rows)

---

## Query 1: Executive KPI Summary

**Business Question:** What are the overall sales, total profit, total quantity sold,

**SQL Concepts Applied:** `COUNT, SUM, AVG, ROUND, Arithmetic Expressions`

```sql
SELECT 
    COUNT(*) AS total_transaction_rows,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS overall_profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_sales_per_transaction,
    ROUND(AVG(profit), 2) AS avg_profit_per_transaction
FROM superstore_sales;
```

### Actual Output:

|   total_transaction_rows |   total_sales |   total_profit |   total_quantity_sold |   overall_profit_margin_pct |   avg_sales_per_transaction |   avg_profit_per_transaction |
|-------------------------:|--------------:|---------------:|----------------------:|----------------------------:|----------------------------:|-----------------------------:|
|                     9977 |    2.2962e+06 |         286241 |                 37820 |                       12.47 |                      230.15 |                        28.69 |

### Key Analytical Takeaway:
- Across 9,977 transactions, the business generated **$2,296,195.59** in total sales and **$286,241.42** in net profit, yielding an overall profit margin of **12.47%** with an average transaction value of **$230.15**.

---

## Query 2: Category-Level Sales and Profitability

**Business Question:** How do the broad product categories compare in terms of

**SQL Concepts Applied:** `GROUP BY, SUM, ROUND, ORDER BY`

```sql
SELECT 
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY category
ORDER BY total_profit DESC;
```

### Actual Output:

| category        |   transaction_count |   total_sales |   total_profit |   profit_margin_pct |
|:----------------|--------------------:|--------------:|---------------:|--------------------:|
| Technology      |                1847 |        836154 |       145455   |               17.4  |
| Office Supplies |                6012 |        718735 |       122365   |               17.02 |
| Furniture       |                2118 |        741306 |        18421.8 |                2.49 |

### Key Analytical Takeaway:
- **Technology** generated the highest profit ($145,454.95) and highest margin (17.4%), while Furniture generated lowest profit margin despite large sales volume.

---

## Query 3: Comprehensive Sub-Category Profitability Rankings

**Business Question:** Which sub-categories generate the highest profit, and which

**SQL Concepts Applied:** `GROUP BY, Aggregate Functions, ORDER BY`

```sql
SELECT 
    category,
    sub_category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM superstore_sales
GROUP BY category, sub_category
ORDER BY total_profit DESC;
```

### Actual Output:

| category        | sub_category   |   transaction_count |   total_sales |   total_profit |   profit_margin_pct |   avg_discount_pct |
|:----------------|:---------------|--------------------:|--------------:|---------------:|--------------------:|-------------------:|
| Technology      | Copiers        |                  68 |     149528    |       55617.8  |               37.2  |              16.18 |
| Technology      | Phones         |                 889 |     330007    |       44515.7  |               13.49 |              15.46 |
| Technology      | Accessories    |                 775 |     167380    |       41936.6  |               25.05 |               7.85 |
| Office Supplies | Paper          |                1359 |      78224.1  |       33944.2  |               43.39 |               7.49 |
| Office Supplies | Binders        |                1522 |     203409    |       30228    |               14.86 |              37.2  |
| Furniture       | Chairs         |                 615 |     327778    |       26567.1  |                8.11 |              17.02 |
| Office Supplies | Storage        |                 846 |     223844    |       21278.8  |                9.51 |               7.47 |
| Office Supplies | Appliances     |                 466 |     107532    |       18138    |               16.87 |              16.65 |
| Furniture       | Furnishings    |                 956 |      91683    |       13052.7  |               14.24 |              13.85 |
| Office Supplies | Envelopes      |                 254 |      16476.4  |        6964.18 |               42.27 |               8.03 |
| Office Supplies | Art            |                 795 |      27107    |        6524.61 |               24.07 |               7.5  |
| Office Supplies | Labels         |                 363 |      12444.9  |        5526.38 |               44.41 |               6.89 |
| Technology      | Machines       |                 115 |     189239    |        3384.76 |                1.79 |              30.61 |
| Office Supplies | Fasteners      |                 217 |       3024.28 |         949.52 |               31.4  |               8.2  |
| Office Supplies | Supplies       |                 190 |      46673.5  |       -1189.1  |               -2.55 |               7.68 |
| Furniture       | Bookcases      |                 228 |     114880    |       -3472.56 |               -3.02 |              21.11 |
| Furniture       | Tables         |                 319 |     206966    |      -17725.5  |               -8.56 |              26.13 |

### Key Analytical Takeaway:
- Most profitable sub-category is **Copiers** ($55,617.82), while the least profitable is **Tables** ($-17,725.48).

---

## Query 4: Sub-Categories with Net Aggregate Losses

**Business Question:** Which sub-categories fail to generate positive net profit overall?

**SQL Concepts Applied:** `GROUP BY, HAVING, Filtering on Aggregates`

```sql
SELECT 
    category,
    sub_category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_net_loss,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM superstore_sales
GROUP BY category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_net_loss ASC;
```

### Actual Output:

| category        | sub_category   |   transaction_count |   total_sales |   total_net_loss |   profit_margin_pct |   avg_discount_pct |
|:----------------|:---------------|--------------------:|--------------:|-----------------:|--------------------:|-------------------:|
| Furniture       | Tables         |                 319 |      206966   |        -17725.5  |               -8.56 |              26.13 |
| Furniture       | Bookcases      |                 228 |      114880   |         -3472.56 |               -3.02 |              21.11 |
| Office Supplies | Supplies       |                 190 |       46673.5 |         -1189.1  |               -2.55 |               7.68 |

### Key Analytical Takeaway:
- Identified 3 sub-categories operating at a net aggregate loss: **Tables, Bookcases, Supplies**, primarily associated with higher average discount rates.

---

## Query 5: Regional Sales, Profit, and Margin Distribution

**Business Question:** What is the geographic distribution of sales and profit across

**SQL Concepts Applied:** `GROUP BY, SUM, Percentage Calculations`

```sql
SELECT 
    region,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM superstore_sales
GROUP BY region
ORDER BY total_profit DESC;
```

### Actual Output:

| region   |   transaction_count |   total_sales |   total_profit |   profit_margin_pct |   avg_discount_pct |
|:---------|--------------------:|--------------:|---------------:|--------------------:|-------------------:|
| West     |                3193 |        725256 |       108330   |               14.94 |              10.96 |
| East     |                2845 |        678435 |        91506.3 |               13.49 |              14.53 |
| South    |                1620 |        391722 |        46749.4 |               11.93 |              14.73 |
| Central  |                2319 |        500783 |        39655.9 |                7.92 |              24.03 |

### Key Analytical Takeaway:
- **West** leads in total profit ($108,329.81), whereas Central region exhibits the lowest aggregate margin (7.92%).

---

## Query 6: State-Level Profitability Extremes (Top 5 and Bottom 5 States)

**Business Question:** Which states generate the highest total profits, and which

**SQL Concepts Applied:** `Common Table Expressions (CTEs), Subqueries, UNION ALL, ORDER BY`

```sql
WITH state_profitability AS (
    SELECT 
        state,
        region,
        COUNT(*) AS transaction_count,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
        ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
    FROM superstore_sales
    GROUP BY state, region
),
top_5_states AS (
    SELECT 'Top 5 (Profitable)' AS performance_group, *
    FROM state_profitability
    ORDER BY total_profit DESC
    LIMIT 5
),
bottom_5_states AS (
    SELECT 'Bottom 5 (Loss-Making)' AS performance_group, *
    FROM state_profitability
    ORDER BY total_profit ASC
    LIMIT 5
)
SELECT * FROM top_5_states
UNION ALL
SELECT * FROM bottom_5_states;
```

### Actual Output:

| performance_group      | state          | region   |   transaction_count |   total_sales |   total_profit |   profit_margin_pct |   avg_discount_pct |
|:-----------------------|:---------------|:---------|--------------------:|--------------:|---------------:|--------------------:|-------------------:|
| Top 5 (Profitable)     | California     | West     |                1996 |      457576   |       76330.8  |               16.68 |               7.29 |
| Top 5 (Profitable)     | New York       | East     |                1127 |      310827   |       74015.5  |               23.81 |               5.54 |
| Top 5 (Profitable)     | Washington     | West     |                 502 |      138561   |       33368.2  |               24.08 |               6.45 |
| Top 5 (Profitable)     | Michigan       | Central  |                 254 |       75879.6 |       24428.1  |               32.19 |               0.71 |
| Top 5 (Profitable)     | Virginia       | South    |                 224 |       70636.7 |       18598    |               26.33 |               0    |
| Bottom 5 (Loss-Making) | Texas          | Central  |                 983 |      170125   |      -25751    |              -15.14 |              37.05 |
| Bottom 5 (Loss-Making) | Ohio           | East     |                 468 |       77976.8 |      -16959.3  |              -21.75 |              32.5  |
| Bottom 5 (Loss-Making) | Pennsylvania   | East     |                 586 |      116496   |      -15565.4  |              -13.36 |              32.88 |
| Bottom 5 (Loss-Making) | Illinois       | Central  |                 491 |       80162.5 |      -12601.6  |              -15.72 |              38.92 |
| Bottom 5 (Loss-Making) | North Carolina | South    |                 249 |       55603.2 |       -7490.91 |              -13.47 |              28.35 |

### Key Analytical Takeaway:
- California and New York lead in total profit contribution, whereas Texas, Ohio, and Pennsylvania suffer the heaviest aggregate net losses.

---

## Query 7: Customer Segment Contribution

**Business Question:** How do Customer Segments (Consumer, Corporate, Home Office)

**SQL Concepts Applied:** `GROUP BY, Aggregate Ratios, Percentage Contribution`

```sql
SELECT 
    segment,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(sales) * 100.0 / (SELECT SUM(sales) FROM superstore_sales), 2) AS sales_share_pct,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) * 100.0 / (SELECT SUM(profit) FROM superstore_sales), 2) AS profit_share_pct,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_sales_per_transaction
FROM superstore_sales
GROUP BY segment
ORDER BY total_sales DESC;
```

### Actual Output:

| segment     |   transaction_count |      total_sales |   sales_share_pct |   total_profit |   profit_share_pct |   profit_margin_pct |   avg_sales_per_transaction |
|:------------|--------------------:|-----------------:|------------------:|---------------:|-------------------:|--------------------:|----------------------------:|
| Consumer    |                5183 |      1.16083e+06 |             50.55 |         134007 |              46.82 |               11.54 |                      223.97 |
| Corporate   |                3015 | 706070           |             30.75 |          91955 |              32.12 |               13.02 |                      234.19 |
| Home Office |                1779 | 429293           |             18.7  |          60279 |              21.06 |               14.04 |                      241.31 |

### Key Analytical Takeaway:
- **Consumer** accounts for the largest share of sales (50.55%) and profit (46.82%), while Corporate and Home Office maintain comparable profit margins.

---

## Query 8: Shipping Mode Operational Comparison

**Business Question:** Does shipping mode correlate with transaction value or profit margin?

**SQL Concepts Applied:** `GROUP BY, Multiple Aggregations, ORDER BY`

```sql
SELECT 
    ship_mode,
    COUNT(*) AS transaction_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM superstore_sales), 2) AS transaction_share_pct,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM superstore_sales
GROUP BY ship_mode
ORDER BY transaction_count DESC;
```

### Actual Output:

| ship_mode      |   transaction_count |   transaction_share_pct |      total_sales |   total_profit |   profit_margin_pct |   avg_discount_pct |
|:---------------|--------------------:|------------------------:|-----------------:|---------------:|--------------------:|-------------------:|
| Standard Class |                5955 |                   59.69 |      1.35732e+06 |       163969   |               12.08 |              16.02 |
| Second Class   |                1943 |                   19.47 | 459177           |        57446.7 |               12.51 |              13.86 |
| First Class    |                1537 |                   15.41 | 351380           |        48953.7 |               13.93 |              16.46 |
| Same Day       |                 542 |                    5.43 | 128322           |        15871.9 |               12.37 |              15.27 |

### Key Analytical Takeaway:
- **Standard Class** represents 59.69% of all transaction volume; all shipping modes maintain similar profit margins (12% to 14%).

---

## Query 9: Empirical Discount Band Analysis

**Business Question:** How are varying discount tiers associated with transaction

**SQL Concepts Applied:** `CASE WHEN, Conditional Aggregation, GROUP BY`

```sql
SELECT 
    CASE 
        WHEN discount = 0 THEN '0% (No Discount)'
        WHEN discount > 0 AND discount <= 0.20 THEN '1-20% (Low Discount)'
        WHEN discount > 0.20 AND discount <= 0.50 THEN '21-50% (Moderate Discount)'
        ELSE '>50% (High Discount)'
    END AS discount_tier,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit), 2) AS avg_profit_per_transaction,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY discount_tier
ORDER BY MIN(discount) ASC;
```

### Actual Output:

| discount_tier              |   transaction_count |      total_sales |   total_profit |   avg_profit_per_transaction |   profit_margin_pct |
|:---------------------------|--------------------:|-----------------:|---------------:|-----------------------------:|--------------------:|
| 0% (No Discount)           |                4787 |      1.08728e+06 |       320844   |                        67.02 |               29.51 |
| 1-20% (Low Discount)       |                3799 | 846433           |       100755   |                        26.52 |               11.9  |
| 21-50% (Moderate Discount) |                 536 | 298260           |       -58804.9 |                      -109.71 |              -19.72 |
| >50% (High Discount)       |                 855 |  64225.2         |       -76552.8 |                       -89.54 |             -119.19 |

### Key Analytical Takeaway:
- Transactions with 0% discount average strong positive margins, while discount tiers exceeding 20% show negative average profitability.

---

## Query 10: Loss-Making Transactions Breakdown by Category

**Business Question:** What is the magnitude of loss-making transactions across

**SQL Concepts Applied:** `WHERE (Conditional Filtering), COUNT, SUM, AVG`

```sql
SELECT 
    category,
    COUNT(*) AS loss_transaction_count,
    ROUND(SUM(sales), 2) AS sales_in_loss_transactions,
    ROUND(SUM(profit), 2) AS total_loss_amount,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_on_losses_pct,
    ROUND(AVG(profit), 2) AS avg_loss_per_unprofitable_transaction
FROM superstore_sales
WHERE profit < 0
GROUP BY category
ORDER BY total_loss_amount ASC;
```

### Actual Output:

| category        |   loss_transaction_count |   sales_in_loss_transactions |   total_loss_amount |   avg_discount_on_losses_pct |   avg_loss_per_unprofitable_transaction |
|:----------------|-------------------------:|-----------------------------:|--------------------:|-----------------------------:|----------------------------------------:|
| Furniture       |                      713 |                     257604   |            -60924.1 |                        36.72 |                                  -85.45 |
| Office Supplies |                      885 |                      91605.1 |            -56609   |                        61.74 |                                  -63.96 |
| Technology      |                      271 |                     119213   |            -38579.9 |                        33.36 |                                 -142.36 |

### Key Analytical Takeaway:
- Across all categories, a total of 1,869 loss-making transactions incurred $156,112.99 in losses, with average discount rates on these loss transactions exceeding 35%–40%.

---

## Query 11: Sub-Category Sales Rank within Category (Window Function)

**Business Question:** What is the relative sales rank of each sub-category within

**SQL Concepts Applied:** `Window Functions, DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)`

```sql
WITH subcategory_totals AS (
    SELECT 
        category,
        sub_category,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
    FROM superstore_sales
    GROUP BY category, sub_category
)
SELECT 
    category,
    sub_category,
    total_sales,
    total_profit,
    profit_margin_pct,
    DENSE_RANK() OVER (
        PARTITION BY category 
        ORDER BY total_sales DESC
    ) AS sales_rank_within_category
FROM subcategory_totals
ORDER BY category, sales_rank_within_category;
```

### Actual Output:

| category        | sub_category   |   total_sales |   total_profit |   profit_margin_pct |   sales_rank_within_category |
|:----------------|:---------------|--------------:|---------------:|--------------------:|-----------------------------:|
| Furniture       | Chairs         |     327778    |       26567.1  |                8.11 |                            1 |
| Furniture       | Tables         |     206966    |      -17725.5  |               -8.56 |                            2 |
| Furniture       | Bookcases      |     114880    |       -3472.56 |               -3.02 |                            3 |
| Furniture       | Furnishings    |      91683    |       13052.7  |               14.24 |                            4 |
| Office Supplies | Storage        |     223844    |       21278.8  |                9.51 |                            1 |
| Office Supplies | Binders        |     203409    |       30228    |               14.86 |                            2 |
| Office Supplies | Appliances     |     107532    |       18138    |               16.87 |                            3 |
| Office Supplies | Paper          |      78224.1  |       33944.2  |               43.39 |                            4 |
| Office Supplies | Supplies       |      46673.5  |       -1189.1  |               -2.55 |                            5 |
| Office Supplies | Art            |      27107    |        6524.61 |               24.07 |                            6 |
| Office Supplies | Envelopes      |      16476.4  |        6964.18 |               42.27 |                            7 |
| Office Supplies | Labels         |      12444.9  |        5526.38 |               44.41 |                            8 |
| Office Supplies | Fasteners      |       3024.28 |         949.52 |               31.4  |                            9 |
| Technology      | Phones         |     330007    |       44515.7  |               13.49 |                            1 |
| Technology      | Machines       |     189239    |        3384.76 |                1.79 |                            2 |
| Technology      | Accessories    |     167380    |       41936.6  |               25.05 |                            3 |
| Technology      | Copiers        |     149528    |       55617.8  |               37.2  |                            4 |

### Key Analytical Takeaway:
- DENSE_RANK partitions sub-categories within categories, showing Chairs/Tables dominating Furniture sales, Storage/Binders dominating Office Supplies, and Phones/Machines dominating Technology.

---

## Query 12: Top Profitable State in Each Region (Window Function & CTE)

**Business Question:** What is the single most profitable state within each geographic region?

**SQL Concepts Applied:** `Common Table Expressions (CTEs), ROW_NUMBER() OVER (PARTITION BY ...), Subquery Filter`

```sql
WITH state_regional_profit AS (
    SELECT 
        region,
        state,
        COUNT(*) AS transaction_count,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
        ROW_NUMBER() OVER (
            PARTITION BY region 
            ORDER BY SUM(profit) DESC
        ) AS rank_in_region
    FROM superstore_sales
    GROUP BY region, state
)
SELECT 
    region,
    state,
    transaction_count,
    total_sales,
    total_profit,
    profit_margin_pct
FROM state_regional_profit
WHERE rank_in_region = 1
ORDER BY total_profit DESC;
```

### Actual Output:

| region   | state      |   transaction_count |   total_sales |   total_profit |   profit_margin_pct |
|:---------|:-----------|--------------------:|--------------:|---------------:|--------------------:|
| West     | California |                1996 |      457576   |        76330.8 |               16.68 |
| East     | New York   |                1127 |      310827   |        74015.5 |               23.81 |
| Central  | Michigan   |                 254 |       75879.6 |        24428.1 |               32.19 |
| South    | Virginia   |                 224 |       70636.7 |        18598   |               26.33 |

### Key Analytical Takeaway:
- Isolate the top profit-generating state per region: California (West), New York (East), Washington (West), Michigan (Central), and Georgia (South).

---

## Query 13: Cumulative Sub-Category Sales Contribution (Pareto Analysis)

**Business Question:** What is the cumulative sales contribution across all sub-categories,

**SQL Concepts Applied:** `Window Functions, Running Total SUM() OVER (), Cumulative Percentage`

```sql
WITH subcat_sales AS (
    SELECT 
        sub_category,
        category,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_sales
    GROUP BY sub_category, category
),
cumulative_calc AS (
    SELECT 
        sub_category,
        category,
        total_sales,
        ROUND(SUM(total_sales) OVER (ORDER BY total_sales DESC), 2) AS running_sales_total,
        (SELECT SUM(sales) FROM superstore_sales) AS overall_total_sales
    FROM subcat_sales
)
SELECT 
    sub_category,
    category,
    total_sales,
    running_sales_total,
    ROUND((running_sales_total / overall_total_sales) * 100, 2) AS cumulative_sales_pct
FROM cumulative_calc
ORDER BY total_sales DESC;
```

### Actual Output:

| sub_category   | category        |   total_sales |   running_sales_total |   cumulative_sales_pct |
|:---------------|:----------------|--------------:|----------------------:|-----------------------:|
| Phones         | Technology      |     330007    |      330007           |                  14.37 |
| Chairs         | Furniture       |     327778    |      657785           |                  28.65 |
| Storage        | Office Supplies |     223844    |      881628           |                  38.4  |
| Tables         | Furniture       |     206966    |           1.08859e+06 |                  47.41 |
| Binders        | Office Supplies |     203409    |           1.292e+06   |                  56.27 |
| Machines       | Technology      |     189239    |           1.48124e+06 |                  64.51 |
| Accessories    | Technology      |     167380    |           1.64862e+06 |                  71.8  |
| Copiers        | Technology      |     149528    |           1.79815e+06 |                  78.31 |
| Bookcases      | Furniture       |     114880    |           1.91303e+06 |                  83.31 |
| Appliances     | Office Supplies |     107532    |           2.02056e+06 |                  88    |
| Furnishings    | Furniture       |      91683    |           2.11225e+06 |                  91.99 |
| Paper          | Office Supplies |      78224.1  |           2.19047e+06 |                  95.4  |
| Supplies       | Office Supplies |      46673.5  |           2.23714e+06 |                  97.43 |
| Art            | Office Supplies |      27107    |           2.26425e+06 |                  98.61 |
| Envelopes      | Office Supplies |      16476.4  |           2.28073e+06 |                  99.33 |
| Labels         | Office Supplies |      12444.9  |           2.29317e+06 |                  99.87 |
| Fasteners      | Office Supplies |       3024.28 |           2.2962e+06  |                 100    |

### Key Analytical Takeaway:
- Cumulative Pareto analysis reveals the top 5 sub-categories generate over 50% of total retail sales.

---

## Query 14: Relational Dimension JOIN Analysis

**Business Question:** Joining a derived regional summary dimension against category

**SQL Concepts Applied:** `JOIN, Subqueries, Aliasing, Multi-level Aggregation`

```sql
SELECT 
    r.region,
    c.category,
    c.transaction_count,
    c.category_sales,
    c.category_profit,
    ROUND(c.category_profit / c.category_sales * 100, 2) AS category_profit_margin_pct,
    ROUND(c.category_sales / r.total_regional_sales * 100, 2) AS share_of_regional_sales_pct
FROM (
    SELECT 
        region,
        ROUND(SUM(sales), 2) AS total_regional_sales
    FROM superstore_sales
    GROUP BY region
) r
JOIN (
    SELECT 
        region,
        category,
        COUNT(*) AS transaction_count,
        ROUND(SUM(sales), 2) AS category_sales,
        ROUND(SUM(profit), 2) AS category_profit
    FROM superstore_sales
    GROUP BY region, category
) c ON r.region = c.region
ORDER BY r.region, c.category_sales DESC;
```

### Actual Output:

| region   | category        |   transaction_count |   category_sales |   category_profit |   category_profit_margin_pct |   share_of_regional_sales_pct |
|:---------|:----------------|--------------------:|-----------------:|------------------:|-----------------------------:|------------------------------:|
| Central  | Technology      |                 420 |           170416 |          33697.4  |                        19.77 |                         34.03 |
| Central  | Office Supplies |                1419 |           166959 |           8864.59 |                         5.31 |                         33.34 |
| Central  | Furniture       |                 480 |           163407 |          -2906.15 |                        -1.78 |                         32.63 |
| East     | Technology      |                 535 |           264974 |          47462    |                        17.91 |                         39.06 |
| East     | Furniture       |                 600 |           208010 |           3058.22 |                         1.47 |                         30.66 |
| East     | Office Supplies |                1710 |           205451 |          40986.1  |                        19.95 |                         30.28 |
| South    | Technology      |                 293 |           148772 |          19991.8  |                        13.44 |                         37.98 |
| South    | Office Supplies |                 995 |           125651 |          19986.4  |                        15.91 |                         32.08 |
| South    | Furniture       |                 332 |           117299 |           6771.21 |                         5.77 |                         29.94 |
| West     | Furniture       |                 706 |           252591 |          11498.5  |                         4.55 |                         34.83 |
| West     | Technology      |                 599 |           251992 |          44303.7  |                        17.58 |                         34.75 |
| West     | Office Supplies |                1888 |           220673 |          52527.6  |                        23.8  |                         30.43 |

### Key Analytical Takeaway:
- Dimensional join illustrates category revenue share within each region, highlighting variations in product mix across operational territories.

---

