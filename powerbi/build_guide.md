# Step-by-Step Guide: Building the Power BI Dashboard

Follow this 15-minute tutorial to construct the interactive dashboard in Power BI Desktop on Windows.

---

## Step 1: Open Power BI Desktop & Load Cleaned Data
1. Launch **Power BI Desktop**.
2. Select **Get Data** > **Text/CSV**.
3. Browse to and select `data/cleaned/Superstore_Cleaned.csv`.
4. Click **Transform Data** in the preview dialog.
5. In Power Query Editor, verify data types:
   - `Postal Code` -> Text
   - `Sales`, `Discount`, `Profit`, `Profit_Margin` -> Decimal Number
   - `Quantity` -> Whole Number
   - `Category`, `Sub-Category`, `Region`, `State`, `Segment`, `Ship Mode`, `Discount_Tier` -> Text
6. Click **Close & Apply** in the top-left corner.

---

## Step 2: Create the Centralized Measures Table
1. On the **Home** ribbon, click **Enter Data**.
2. Set the table name to `_Measures` and click **Load**.
3. For each formula in `powerbi/dax_measures.dax`:
   - Right-click `_Measures` > **New Measure**.
   - Paste the DAX code.
   - Set the proper data format (Currency `$`, Percentage `%`, or Whole Number).
4. Hide the empty placeholder column `Column1` in `_Measures` to make it a pure measure group folder.

---

## Step 3: Insert Top KPI Cards
1. Add a **Card** visual to the top left of the canvas.
2. Drag `[Total Sales]` from `_Measures` into the Fields well.
3. Under Format Visual > General > Title, set Title to "Total Sales".
4. Repeat to create 4 more adjacent KPI cards:
   - `[Total Profit]` (Title: "Total Profit")
   - `[Profit Margin %]` (Title: "Profit Margin")
   - `[Total Transactions]` (Title: "Total Transactions")
   - `[Loss Transaction Share %]` (Title: "Loss Transaction Share")
5. Align the 5 cards horizontally across the top banner.

---

## Step 4: Build Visual 1 — Category Performance
1. Insert a **Clustered Column Chart**.
2. Drag `Superstore_Cleaned[Category]` to the **X-axis**.
3. Drag `[Total Sales]` and `[Total Profit]` to the **Y-axis**.
4. In formatting, enable **Data Labels**.

---

## Step 5: Build Visual 2 — Sub-Category Profitability Rankings
1. Insert a **Clustered Bar Chart**.
2. Drag `Superstore_Cleaned[Sub-Category]` to the **Y-axis**.
3. Drag `[Total Profit]` to the **X-axis**.
4. Sort axis by `[Total Profit]` descending.
5. In formatting > Bars > Color > Click the `fx` (Conditional Formatting) button:
   - Format style: **Field value**
   - What field should we base this on? Select `_Measures[SubCategory Profit Color]`.
   - Now, loss-making bars (Tables, Bookcases, Supplies) will render red, and profitable bars will render blue!

---

## Step 6: Build Visual 3 — State Profit Extremes
1. Insert a **Clustered Bar Chart**.
2. Drag `Superstore_Cleaned[State]` to the **Y-axis**.
3. Drag `[Total Profit]` to the **X-axis**.
4. In the Filters pane under `State`:
   - Filter type: **Top N**
   - Show items: **Top 5** by `[Total Profit]`.
5. Duplicate or create an adjacent chart showing **Bottom 5** states by `[Total Profit]`.

---

## Step 7: Build Visual 4 — Discount vs. Profit Margin
1. Insert a **Line and Clustered Column Chart**.
2. Drag `Superstore_Cleaned[Discount_Tier]` to the **X-axis**.
3. Drag `[Total Sales]` to **Column y-axis**.
4. Drag `[Profit Margin %]` to **Line y-axis**.
5. Enable Data Labels for both series.

---

## Step 8: Add Interactive Slicers
1. Add 4 **Slicer** visuals along the left or bottom:
   - Slicer 1: `Superstore_Cleaned[Region]`
   - Slicer 2: `Superstore_Cleaned[Category]`
   - Slicer 3: `Superstore_Cleaned[Segment]`
   - Slicer 4: `Superstore_Cleaned[Ship Mode]`
2. Test clicking "Central" region: observe how the visuals dynamically filter to reveal the heavy losses in Texas and Illinois, and the 24% average discount rate!

---

## Step 9: Save & Publish
1. Click **File** > **Save As** > `Retail_Sales_Performance_Dashboard.pbix`.
2. (Optional) Click **Publish** to publish to Power BI Service for sharing and portfolio demonstration.
