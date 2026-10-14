# Power BI Dashboard Visual Specifications & Layout Architecture

**Target Canvas:** 16:9 Standard Dashboard (1280 x 720 px or 1920 x 1080 px)  
**Theme Palettes:** Slate Blue (`#2b5c8f`), Forest Green (`#2ca02c`), Crimson Red (`#d62728`), Charcoal Gray (`#333333`)

---

## 1. Dashboard Layout Wireframe

```
+-----------------------------------------------------------------------------------------------+
|  HEADER: Retail Sales & Profitability Analytics Dashboard        [Slicers: Region | Category] |
+-----------------------------------------------------------------------------------------------+
|  [ KPI 1 ]       |  [ KPI 2 ]       |  [ KPI 3 ]       |  [ KPI 4 ]       |  [ KPI 5 ]        |
|  Total Sales     |  Total Profit    |  Profit Margin % |  Transactions    |  Loss Trans. Share|
|  $2.30M          |  $286.24K        |  12.47%          |  9,977           |  18.73%           |
+-------------------------------------+---------------------------------------------------------+
|  VISUAL 1: Category Sales vs Profit |  VISUAL 2: Sub-Category Profit Breakdown                |
|  (Clustered Column Chart)           |  (Horizontal Bar Chart with Conditional Red/Blue)       |
|                                     |                                                         |
+-------------------------------------+---------------------------------------------------------+
|  VISUAL 3: State Profit Extremes    |  VISUAL 4: Discount Tier vs. Margin Impact              |
|  (Top 5 & Bottom 5 Bar Chart)       |  (Column / Line Combo Chart)                            |
|                                     |                                                         |
+-------------------------------------+---------------------------------------------------------+
|  VISUAL 5: Customer Segment Metrics |  SLICER BAR (Bottom or Left):                           |
|  (Donut / Treemap Visual)           |  [Segment: All]  [Ship Mode: All]  [Discount Tier: All]   |
+-------------------------------------+---------------------------------------------------------+
```

---

## 2. Visual Component Detailed Configuration

### Section A: Top KPI Banner (5 Card Visuals)
1. **Card 1 — Total Sales:**
   - Field: `[Total Sales]`
   - Display Units: Auto (shows `$2.30M`)
   - Title: "Total Sales"
2. **Card 2 — Total Net Profit:**
   - Field: `[Total Profit]`
   - Display Units: Auto (shows `$286.24K`)
   - Title: "Total Profit"
3. **Card 3 — Profit Margin %:**
   - Field: `[Profit Margin %]`
   - Format: `0.00%` (shows `12.47%`)
   - Title: "Profit Margin"
4. **Card 4 — Total Transactions:**
   - Field: `[Total Transactions]`
   - Format: Integer with comma (shows `9,977`)
   - Title: "Total Transactions"
5. **Card 5 — Loss-Making Share:**
   - Field: `[Loss Transaction Share %]`
   - Format: `0.00%` (shows `18.73%`)
   - Title: "Loss Transaction Share"

---

### Section B: Main Analytical Visuals

#### Visual 1: Category Sales vs. Net Profit (Clustered Column Chart)
- **Visual Type:** Clustered column chart
- **X-Axis:** `Superstore_Cleaned[Category]`
- **Y-Axis:** `[Total Sales]`, `[Total Profit]`
- **Colors:** Sales (`#2b5c8f`), Profit (`#2ca02c`)
- **Data Labels:** On, Display units = Thousands (`$k`)
- **Insight Displayed:** Illustrates that Furniture produces comparable sales to Technology and Office Supplies, but yields very low net profit.

#### Visual 2: Sub-Category Profit Rankings (Horizontal Bar Chart)
- **Visual Type:** Clustered bar chart
- **Y-Axis:** `Superstore_Cleaned[Sub-Category]` (Sorted by `[Total Profit]` descending)
- **X-Axis:** `[Total Profit]`
- **Data Colors:** Conditional Formatting > Field Value > `_Measures[SubCategory Profit Color]`
- **Insight Displayed:** Highlights profitable sub-categories (Copiers, Phones, Accessories) in blue, and loss-making sub-categories (Tables, Bookcases, Supplies) in distinct red.

#### Visual 3: State Profit Extremes (Horizontal Bar Chart)
- **Visual Type:** Clustered bar chart
- **Y-Axis:** `Superstore_Cleaned[State]`
- **X-Axis:** `[Total Profit]`
- **Filters:** Top N State Filter (Top 5 by `[Total Profit]`) OR bottom N (Bottom 5).
- **Insight Displayed:** Spotlights strong contributors (California, New York) vs. heavy loss centers (Texas, Ohio, Pennsylvania, Illinois).

#### Visual 4: Discount Tier Profitability Impact (Clustered Column & Line Chart)
- **Visual Type:** Line and clustered column chart
- **Shared X-Axis:** `Superstore_Cleaned[Discount_Tier]` (0%, 1-20%, 21-50%, >50%)
- **Column Values (Y1):** `[Total Sales]`
- **Line Values (Y2):** `[Profit Margin %]`
- **Insight Displayed:** Shows dramatic plunge in profit margin from +29.5% at 0% discount down to negative margins once discount exceeds 20%.

#### Visual 5: Customer Segment Volume & Profit Share (Donut / Matrix Chart)
- **Visual Type:** Donut chart or Matrix Table
- **Legend / Rows:** `Superstore_Cleaned[Segment]`
- **Values:** `[Total Sales]`, `[Total Profit]`, `[Profit Margin %]`
- **Insight Displayed:** Validates that Consumer accounts for ~50% of volume while Corporate and Home Office maintain higher profit margins.

---

### Section C: Interactive Slicers
1. **Region Slicer:** Dropdown or Horizontal tile (`Central`, `East`, `South`, `West`).
2. **Category Slicer:** Dropdown (`Furniture`, `Office Supplies`, `Technology`).
3. **Segment Slicer:** Tile (`Consumer`, `Corporate`, `Home Office`).
4. **Ship Mode Slicer:** Dropdown (`Standard Class`, `Second Class`, `First Class`, `Same Day`).
