-- sql/schema.sql
-- Relational Database Schema for Retail Sales Analytics
-- Target Database: SQLite 3

DROP TABLE IF EXISTS superstore_sales;

CREATE TABLE superstore_sales (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ship_mode VARCHAR(50) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    region VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    sales DECIMAL(10, 4) NOT NULL,
    quantity INTEGER NOT NULL,
    discount DECIMAL(5, 4) NOT NULL,
    profit DECIMAL(10, 4) NOT NULL,
    profit_margin DECIMAL(6, 4) NOT NULL,
    discount_tier VARCHAR(30) NOT NULL
);

-- Indexes for analytical query optimization
CREATE INDEX idx_sales_category ON superstore_sales(category);
CREATE INDEX idx_sales_sub_category ON superstore_sales(sub_category);
CREATE INDEX idx_sales_region ON superstore_sales(region);
CREATE INDEX idx_sales_state ON superstore_sales(state);
CREATE INDEX idx_sales_segment ON superstore_sales(segment);
CREATE INDEX idx_sales_discount_tier ON superstore_sales(discount_tier);
