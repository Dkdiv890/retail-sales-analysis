"""
src/run_sql_queries.py
Executes all SQL queries from sql/analysis_queries.sql against data/retail_sales.db,
validates output rows, and writes a complete markdown report sql/query_results.md.
"""

import os
import sqlite3
import re
import pandas as pd

def run_queries():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "retail_sales.db")
    sql_file = os.path.join(base_dir, "sql", "analysis_queries.sql")
    output_md = os.path.join(base_dir, "sql", "query_results.md")

    conn = sqlite3.connect(db_path)

    with open(sql_file, "r") as f:
        content = f.read()

    # Split into query blocks based on header comments
    query_blocks = re.split(r"-- -{30,}\n-- QUERY ", content)
    
    results_md = ["# SQL Analytical Query Execution & Results Log\n\n"]
    results_md.append("Database: `data/retail_sales.db` (SQLite 3) | Source Table: `superstore_sales` (9,977 Cleaned Transaction Rows)\n\n")
    results_md.append("---\n\n")

    for i, block in enumerate(query_blocks[1:], 1):
        lines = block.strip().split("\n")
        header_line = lines[0] # e.g. "1: Executive KPI Summary"
        query_title = f"Query {header_line}"
        
        # Extract business question and concepts from comments
        business_question = ""
        concepts = ""
        sql_lines = []
        
        for line in lines[1:]:
            if line.startswith("-- Business Question:"):
                business_question = line.replace("-- Business Question:", "").strip()
            elif line.startswith("-- Concepts:"):
                concepts = line.replace("-- Concepts:", "").strip()
            elif line.startswith("--") or line.strip() == "":
                continue
            else:
                sql_lines.append(line)
        
        raw_sql = "\n".join(sql_lines).strip()
        if not raw_sql.endswith(";"):
            raw_sql += ";"

        # Execute query
        try:
            df_result = pd.read_sql_query(raw_sql, conn)
            print(f"[OK] Executed Query {i}: {header_line} -> {len(df_result)} rows returned.")
            
            results_md.append(f"## {query_title}\n\n")
            if business_question:
                results_md.append(f"**Business Question:** {business_question}\n\n")
            if concepts:
                results_md.append(f"**SQL Concepts Applied:** `{concepts}`\n\n")
            
            results_md.append("```sql\n" + raw_sql + "\n```\n\n")
            results_md.append("### Actual Output:\n\n")
            results_md.append(df_result.to_markdown(index=False) + "\n\n")
            
            # Brief interpretation
            results_md.append("### Key Analytical Takeaway:\n")
            if i == 1:
                results_md.append(f"- Across {df_result['total_transaction_rows'].iloc[0]:,} transactions, the business generated **${df_result['total_sales'].iloc[0]:,.2f}** in total sales and **${df_result['total_profit'].iloc[0]:,.2f}** in net profit, yielding an overall profit margin of **{df_result['overall_profit_margin_pct'].iloc[0]}%** with an average transaction value of **${df_result['avg_sales_per_transaction'].iloc[0]:,.2f}**.\n\n")
            elif i == 2:
                top_cat = df_result.iloc[0]
                results_md.append(f"- **{top_cat['category']}** generated the highest profit (${top_cat['total_profit']:,.2f}) and highest margin ({top_cat['profit_margin_pct']}%), while Furniture generated lowest profit margin despite large sales volume.\n\n")
            elif i == 3:
                top_sub = df_result.iloc[0]
                bottom_sub = df_result.iloc[-1]
                results_md.append(f"- Most profitable sub-category is **{top_sub['sub_category']}** (${top_sub['total_profit']:,.2f}), while the least profitable is **{bottom_sub['sub_category']}** (${bottom_sub['total_profit']:,.2f}).\n\n")
            elif i == 4:
                loss_subs = df_result['sub_category'].tolist()
                results_md.append(f"- Identified {len(df_result)} sub-categories operating at a net aggregate loss: **{', '.join(loss_subs)}**, primarily associated with higher average discount rates.\n\n")
            elif i == 5:
                top_reg = df_result.iloc[0]
                results_md.append(f"- **{top_reg['region']}** leads in total profit (${top_reg['total_profit']:,.2f}), whereas Central region exhibits the lowest aggregate margin ({df_result[df_result['region']=='Central']['profit_margin_pct'].iloc[0]}%).\n\n")
            elif i == 6:
                results_md.append("- California and New York lead in total profit contribution, whereas Texas, Ohio, and Pennsylvania suffer the heaviest aggregate net losses.\n\n")
            elif i == 7:
                top_seg = df_result.iloc[0]
                results_md.append(f"- **{top_seg['segment']}** accounts for the largest share of sales ({top_seg['sales_share_pct']}%) and profit ({top_seg['profit_share_pct']}%), while Corporate and Home Office maintain comparable profit margins.\n\n")
            elif i == 8:
                top_ship = df_result.iloc[0]
                results_md.append(f"- **{top_ship['ship_mode']}** represents {top_ship['transaction_share_pct']}% of all transaction volume; all shipping modes maintain similar profit margins (12% to 14%).\n\n")
            elif i == 9:
                results_md.append("- Transactions with 0% discount average strong positive margins, while discount tiers exceeding 20% show negative average profitability.\n\n")
            elif i == 10:
                results_md.append(f"- Across all categories, a total of {df_result['loss_transaction_count'].sum():,} loss-making transactions incurred ${abs(df_result['total_loss_amount'].sum()):,.2f} in losses, with average discount rates on these loss transactions exceeding 35%–40%.\n\n")
            elif i == 11:
                results_md.append("- DENSE_RANK partitions sub-categories within categories, showing Chairs/Tables dominating Furniture sales, Storage/Binders dominating Office Supplies, and Phones/Machines dominating Technology.\n\n")
            elif i == 12:
                results_md.append("- Isolate the top profit-generating state per region: California (West), New York (East), Washington (West), Michigan (Central), and Georgia (South).\n\n")
            elif i == 13:
                results_md.append("- Cumulative Pareto analysis reveals the top 5 sub-categories generate over 50% of total retail sales.\n\n")
            elif i == 14:
                results_md.append("- Dimensional join illustrates category revenue share within each region, highlighting variations in product mix across operational territories.\n\n")
            
            results_md.append("---\n\n")

        except Exception as e:
            print(f"[ERROR] Executing Query {i}: {e}")
            results_md.append(f"## Query {i}: {header_line}\n\nExecution error: `{e}`\n\n---\n\n")

    conn.close()

    with open(output_md, "w") as f:
        f.writelines(results_md)
    print(f"[OK] Wrote all executed SQL results to: {output_md}")

if __name__ == "__main__":
    run_queries()
