import os
import sqlite3
import pandas as pd

def setup_database():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "retail_sales.db")
    schema_path = os.path.join(base_dir, "sql", "schema.sql")
    cleaned_csv_path = os.path.join(base_dir, "data", "cleaned", "Superstore_Cleaned.csv")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(schema_path, "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    df = pd.read_csv(cleaned_csv_path)
    
    col_mapping = {
        "Ship Mode": "ship_mode",
        "Segment": "segment",
        "Country": "country",
        "City": "city",
        "State": "state",
        "Postal Code": "postal_code",
        "Region": "region",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
        "Profit_Margin": "profit_margin",
        "Discount_Tier": "discount_tier"
    }
    df_sql = df.rename(columns=col_mapping)

    df_sql.to_sql("superstore_sales", conn, if_exists="append", index=False)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM superstore_sales;")
    row_count = cursor.fetchone()[0]
    print(f"[OK] {row_count:,} rows loaded into 'superstore_sales'.")

    conn.close()

if __name__ == "__main__":
    setup_database()
