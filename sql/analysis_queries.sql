-- ==============================================================================
-- sql/analysis_queries.sql
-- Comprehensive SQL Analytical Queries for Retail Sales Analysis
-- Database: SQLite 3 | Table: superstore_sales (9,977 transaction rows)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Executive KPI Summary
-- Business Question: What are the overall sales, total profit, total quantity sold,
-- transaction-row count, and overall profit margin across the entire dataset?
-- Concepts: COUNT, SUM, AVG, ROUND, Arithmetic Expressions
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_transaction_rows,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS overall_profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_sales_per_transaction,
    ROUND(AVG(profit), 2) AS avg_profit_per_transaction
FROM superstore_sales;


-- ------------------------------------------------------------------------------
-- QUERY 2: Category-Level Sales and Profitability
-- Business Question: How do the broad product categories compare in terms of 
-- sales volume, net profit, and profit margin?
-- Concepts: GROUP BY, SUM, ROUND, ORDER BY
-- ------------------------------------------------------------------------------
SELECT 
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY category
ORDER BY total_profit DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Comprehensive Sub-Category Profitability Rankings
-- Business Question: Which sub-categories generate the highest profit, and which
-- ones produce low or negative margins?
-- Concepts: GROUP BY, Aggregate Functions, ORDER BY
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 4: Sub-Categories with Net Aggregate Losses
-- Business Question: Which sub-categories fail to generate positive net profit overall?
-- Concepts: GROUP BY, HAVING, Filtering on Aggregates
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 5: Regional Sales, Profit, and Margin Distribution
-- Business Question: What is the geographic distribution of sales and profit across 
-- the four major operational regions?
-- Concepts: GROUP BY, SUM, Percentage Calculations
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 6: State-Level Profitability Extremes (Top 5 and Bottom 5 States)
-- Business Question: Which states generate the highest total profits, and which
-- states incur the heaviest net losses?
-- Concepts: Common Table Expressions (CTEs), Subqueries, UNION ALL, ORDER BY
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 7: Customer Segment Contribution
-- Business Question: How do Customer Segments (Consumer, Corporate, Home Office)
-- contribute to overall sales and profit volume?
-- Concepts: GROUP BY, Aggregate Ratios, Percentage Contribution
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 8: Shipping Mode Operational Comparison
-- Business Question: Does shipping mode correlate with transaction value or profit margin?
-- Concepts: GROUP BY, Multiple Aggregations, ORDER BY
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 9: Empirical Discount Band Analysis
-- Business Question: How are varying discount tiers associated with transaction 
-- profitability and profit margins?
-- Concepts: CASE WHEN, Conditional Aggregation, GROUP BY
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 10: Loss-Making Transactions Breakdown by Category
-- Business Question: What is the magnitude of loss-making transactions across 
-- categories, and what average discount was applied to those unprofitable transactions?
-- Concepts: WHERE (Conditional Filtering), COUNT, SUM, AVG
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 11: Sub-Category Sales Rank within Category (Window Function)
-- Business Question: What is the relative sales rank of each sub-category within
-- its parent category?
-- Concepts: Window Functions, DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 12: Top Profitable State in Each Region (Window Function & CTE)
-- Business Question: What is the single most profitable state within each geographic region?
-- Concepts: Common Table Expressions (CTEs), ROW_NUMBER() OVER (PARTITION BY ...), Subquery Filter
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 13: Cumulative Sub-Category Sales Contribution (Pareto Analysis)
-- Business Question: What is the cumulative sales contribution across all sub-categories,
-- and which sub-categories account for the bulk of revenue?
-- Concepts: Window Functions, Running Total SUM() OVER (), Cumulative Percentage
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- QUERY 14: Relational Dimension JOIN Analysis
-- Business Question: Joining a derived regional summary dimension against category 
-- metrics to inspect category profit contribution across regions.
-- Concepts: JOIN, Subqueries, Aliasing, Multi-level Aggregation
-- ------------------------------------------------------------------------------
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
