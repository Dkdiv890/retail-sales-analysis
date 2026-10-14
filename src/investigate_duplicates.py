import pandas as pd
import numpy as np

def analyze():
    df = pd.read_csv("SampleSuperstore.csv")
    total_rows = len(df)
    dup_mask = df.duplicated(keep=False)
    num_dup_rows = df.duplicated().sum()
    all_dups = df[dup_mask].sort_values(by=["State", "City", "Sub-Category", "Sales"])

    sales_before = df["Sales"].sum()
    profit_before = df["Profit"].sum()
    qty_before = df["Quantity"].sum()
    margin_before = (profit_before / sales_before) * 100

    df_dedup = df.drop_duplicates(keep="first")
    sales_after = df_dedup["Sales"].sum()
    profit_after = df_dedup["Profit"].sum()
    qty_after = df_dedup["Quantity"].sum()
    margin_after = (profit_after / sales_after) * 100
    rows_after = len(df_dedup)

    sales_diff = sales_before - sales_after
    profit_diff = profit_before - profit_after
    qty_diff = qty_before - qty_after
    margin_diff = margin_after - margin_before

    print(f"Total Raw Rows: {total_rows}")
    print(f"Total Extra Duplicate Occurrences: {num_dup_rows}")
    print(f"Total Rows involved in duplicates: {len(all_dups)}")
    print(f"Cleaned Rows: {rows_after}")
    print("="*60)
    print(f"Sales Before:   ${sales_before:,.2f}")
    print(f"Sales After:    ${sales_after:,.2f}")
    print(f"Sales Delta:    -${sales_diff:,.2f} (-{sales_diff/sales_before*100:.4f}%)")
    print("="*60)
    print(f"Profit Before:  ${profit_before:,.2f}")
    print(f"Profit After:   ${profit_after:,.2f}")
    print(f"Profit Delta:   -${profit_diff:,.2f} (-{profit_diff/profit_before*100:.4f}%)")
    print("="*60)
    print(f"Quantity Before: {qty_before:,}")
    print(f"Quantity After:  {qty_after:,}")
    print(f"Quantity Delta:  -{qty_diff:,} (-{qty_diff/qty_before*100:.4f}%)")
    print("="*60)
    print(f"Margin Before:  {margin_before:.4f}%")
    print(f"Margin After:   {margin_after:.4f}%")
    print(f"Margin Delta:   +{margin_diff:.4f}%")
    print("="*60)
    print("\nAll Duplicate Rows Inspected:")
    print(all_dups[["Ship Mode", "Segment", "City", "State", "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"]].to_string())

if __name__ == "__main__":
    analyze()
