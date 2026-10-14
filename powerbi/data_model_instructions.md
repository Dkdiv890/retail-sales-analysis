# Power BI Data Modeling & Setup Instructions

## 1. Environment & Architecture Clarification
> [!IMPORTANT]
> **Dashboard Delivery Notice:**  
> Power BI Desktop is a Windows-based desktop application. In this macOS/Linux command-line environment, a proprietary binary `.pbix` file cannot be opened, rendered, or automated directly without an active Power BI Desktop installation on Windows.  
> 
> To ensure **100% reproducibility and completeness**, this project provides:
> 1. Cleaned, validated CSV source files in `data/cleaned/Superstore_Cleaned.csv`
> 2. Complete, validated DAX formulas in `powerbi/dax_measures.dax`
> 3. Comprehensive visual placement, layout coordinates, and formatting specs in `powerbi/dashboard_visual_specifications.md`
> 4. Step-by-step assembly guide in `powerbi/build_guide.md`
> 5. Excel-compatible aggregated datasets in `data/exports/`

---

## 2. Ingesting Data into Power BI Desktop
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select the file: `data/cleaned/Superstore_Cleaned.csv`.
4. Click **Transform Data** (opens Power Query Editor).
5. Verify column data types:
   - `Postal Code`: Text (`type text`)
   - `Ship Mode`, `Segment`, `Country`, `City`, `State`, `Region`, `Category`, `Sub-Category`, `Discount_Tier`: Text (`type text`)
   - `Sales`, `Discount`, `Profit`, `Profit_Margin`: Fixed Decimal Number / Decimal (`type number`)
   - `Quantity`: Whole Number (`Int64.Type`)
6. Click **Close & Apply**.

---

## 3. Data Model Architecture

### Recommended Modeling Options:
- **Option A (Single Fact Table - Direct Analytical Table Model):**
  - Use `Superstore_Cleaned` directly as the core analytical table.
  - Create a dedicated measure table called `_Measures` to store all DAX metrics cleanly.
- **Option B (Star Schema - Optional Advanced Modeling):**
  - **Fact Table:** `Fact_Sales` (Transaction row metrics: Sales, Quantity, Discount, Profit).
  - **Dimension Table 1:** `Dim_Geography` (State, City, Postal Code, Region).
  - **Dimension Table 2:** `Dim_Category` (Category, Sub-Category).
  - **Dimension Table 3:** `Dim_CustomerSegment` (Segment).
  - **Relationships:** 1-to-many single direction from dimensions to `Fact_Sales`.

---

## 4. Creating the `_Measures` Table
1. In the Power BI **Home** tab, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` > **New Measure**.
4. Copy and paste each measure from `powerbi/dax_measures.dax`.
5. Format metrics:
   - `Total Sales`, `Total Profit`, `Avg Sales Per Transaction`: Format as **Currency ($)** with 2 decimal places.
   - `Profit Margin %`, `Loss Transaction Share %`, `Avg Discount Rate`: Format as **Percentage (%)** with 2 decimal places.
   - `Total Transactions`, `Total Quantity`, `Loss-Making Transactions`: Format as **Whole Number** with thousands separator.
