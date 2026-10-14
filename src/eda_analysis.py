import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

def generate_eda():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_csv = os.path.join(base_dir, "data", "cleaned", "Superstore_Cleaned.csv")
    visuals_dir = os.path.join(base_dir, "visuals")
    exports_dir = os.path.join(base_dir, "data", "exports")
    os.makedirs(visuals_dir, exist_ok=True)
    os.makedirs(exports_dir, exist_ok=True)

    df = pd.read_csv(cleaned_csv)

    # 1. Generate Summary CSV Exports
    cat_summary = df.groupby("Category").agg(
        Transaction_Count=("Sales", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    cat_summary["Profit_Margin_Pct"] = (cat_summary["Total_Profit"] / cat_summary["Total_Sales"] * 100).round(2)
    cat_summary["Total_Sales"] = cat_summary["Total_Sales"].round(2)
    cat_summary["Total_Profit"] = cat_summary["Total_Profit"].round(2)
    cat_summary.to_csv(os.path.join(exports_dir, "category_summary.csv"), index=False)

    subcat_summary = df.groupby(["Category", "Sub-Category"]).agg(
        Transaction_Count=("Sales", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    subcat_summary["Profit_Margin_Pct"] = (subcat_summary["Total_Profit"] / subcat_summary["Total_Sales"] * 100).round(2)
    subcat_summary["Total_Sales"] = subcat_summary["Total_Sales"].round(2)
    subcat_summary["Total_Profit"] = subcat_summary["Total_Profit"].round(2)
    subcat_summary.sort_values(by="Total_Profit", ascending=False).to_csv(
        os.path.join(exports_dir, "subcategory_summary.csv"), index=False
    )

    reg_summary = df.groupby("Region").agg(
        Transaction_Count=("Sales", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()
    reg_summary["Profit_Margin_Pct"] = (reg_summary["Total_Profit"] / reg_summary["Total_Sales"] * 100).round(2)
    reg_summary["Total_Sales"] = reg_summary["Total_Sales"].round(2)
    reg_summary["Total_Profit"] = reg_summary["Total_Profit"].round(2)
    reg_summary.to_csv(os.path.join(exports_dir, "regional_summary.csv"), index=False)

    seg_summary = df.groupby("Segment").agg(
        Transaction_Count=("Sales", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Transaction_Sales=("Sales", "mean")
    ).reset_index()
    seg_summary["Profit_Margin_Pct"] = (seg_summary["Total_Profit"] / seg_summary["Total_Sales"] * 100).round(2)
    seg_summary["Total_Sales"] = seg_summary["Total_Sales"].round(2)
    seg_summary["Total_Profit"] = seg_summary["Total_Profit"].round(2)
    seg_summary["Avg_Transaction_Sales"] = seg_summary["Avg_Transaction_Sales"].round(2)
    seg_summary.to_csv(os.path.join(exports_dir, "segment_summary.csv"), index=False)

    disc_summary = df.groupby("Discount_Tier").agg(
        Transaction_Count=("Sales", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Profit_Per_Transaction=("Profit", "mean")
    ).reset_index()
    disc_summary["Profit_Margin_Pct"] = (disc_summary["Total_Profit"] / disc_summary["Total_Sales"] * 100).round(2)
    disc_summary["Total_Sales"] = disc_summary["Total_Sales"].round(2)
    disc_summary["Total_Profit"] = disc_summary["Total_Profit"].round(2)
    disc_summary["Avg_Profit_Per_Transaction"] = disc_summary["Avg_Profit_Per_Transaction"].round(2)
    disc_summary.to_csv(os.path.join(exports_dir, "discount_tier_summary.csv"), index=False)

    # 2. Visualizations
    # Chart 1: Category Sales and Profit Comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    cat_plot = cat_summary.sort_values(by="Total_Sales", ascending=False)
    x = np.arange(len(cat_plot))
    width = 0.35

    rects1 = ax.bar(x - width/2, cat_plot["Total_Sales"] / 1000, width, label="Sales ($k)", color="#2b5c8f")
    rects2 = ax.bar(x + width/2, cat_plot["Total_Profit"] / 1000, width, label="Profit ($k)", color="#2ca02c")

    ax.set_ylabel("Amount ($ in Thousands)")
    ax.set_title("Total Sales vs. Net Profit by Category", weight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_plot["Category"])
    ax.legend(frameon=True)

    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"${h:.1f}k", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"${h:.1f}k", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, "01_category_sales_profit.png"))
    plt.close()

    # Chart 2: Sub-Category Profitability (Red = Net Loss)
    subcat_sorted = subcat_summary.sort_values(by="Total_Profit", ascending=True)
    colors = ["#d62728" if p < 0 else "#1f77b4" for p in subcat_sorted["Total_Profit"]]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(subcat_sorted["Sub-Category"], subcat_sorted["Total_Profit"] / 1000, color=colors)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Net Profit ($ in Thousands)")
    ax.set_title("Net Profit by Sub-Category (Red = Net Loss)", weight="bold", pad=12)

    for bar in bars:
        w = bar.get_width()
        ha = "left" if w >= 0 else "right"
        offset = 0.5 if w >= 0 else -0.5
        ax.annotate(f"${w:.1f}k", xy=(w + offset, bar.get_y() + bar.get_height()/2),
                    va="center", ha=ha, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, "02_subcategory_profitability.png"))
    plt.close()

    # Chart 3: Regional Sales, Profit, and Profit Margin %
    reg_sorted = reg_summary.sort_values(by="Total_Profit", ascending=False)
    fig, ax1 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(reg_sorted))
    width = 0.35

    ax1.bar(x - width/2, reg_sorted["Total_Sales"] / 1000, width, label="Sales ($k)", color="#4575b4")
    ax1.bar(x + width/2, reg_sorted["Total_Profit"] / 1000, width, label="Profit ($k)", color="#74add1")
    ax1.set_ylabel("Volume ($ in Thousands)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_sorted["Region"])

    ax2 = ax1.twinx()
    ax2.plot(x, reg_sorted["Profit_Margin_Pct"], color="#d73027", marker="o", linewidth=2.2, label="Margin %")
    ax2.set_ylabel("Profit Margin (%)", color="#d73027")
    ax2.tick_params(axis="y", labelcolor="#d73027")
    ax2.grid(False)

    for i, txt in enumerate(reg_sorted["Profit_Margin_Pct"]):
        ax2.annotate(f"{txt:.1f}%", (x[i], txt), textcoords="offset points", xytext=(0, 6),
                     ha="center", fontsize=9, weight="bold", color="#d73027")

    ax1.set_title("Regional Sales, Profit, and Profit Margin %", weight="bold", pad=12)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, "03_regional_performance.png"))
    plt.close()

    # Chart 4: Top 5 vs Bottom 5 States by Net Profit
    state_perf = df.groupby("State").agg(
        Total_Profit=("Profit", "sum"),
        Total_Sales=("Sales", "sum")
    ).reset_index()
    top5 = state_perf.sort_values(by="Total_Profit", ascending=False).head(5)
    bottom5 = state_perf.sort_values(by="Total_Profit", ascending=True).head(5)
    extremes = pd.concat([bottom5, top5]).sort_values(by="Total_Profit")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bar_colors = ["#d62728" if p < 0 else "#2ca02c" for p in extremes["Total_Profit"]]
    bars = ax.barh(extremes["State"], extremes["Total_Profit"] / 1000, color=bar_colors)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Net Profit ($ in Thousands)")
    ax.set_title("State Profitability Extremes: Top 5 Profitable vs. Bottom 5 Loss-Making", weight="bold", pad=12)

    for bar in bars:
        w = bar.get_width()
        ha = "left" if w >= 0 else "right"
        offset = 1.0 if w >= 0 else -1.0
        ax.annotate(f"${w:.1f}k", xy=(w + offset, bar.get_y() + bar.get_height()/2),
                    va="center", ha=ha, fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, "04_state_extremes.png"))
    plt.close()

    # Chart 5: Discount Levels vs Profit Margin
    disc_rate_summary = df.groupby("Discount").agg(
        Avg_Profit_Margin=("Profit_Margin", "mean"),
        Transaction_Count=("Sales", "count"),
        Total_Profit=("Profit", "sum")
    ).reset_index()

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.plot(disc_rate_summary["Discount"] * 100, disc_rate_summary["Avg_Profit_Margin"] * 100,
            marker="s", color="#b2182b", linewidth=2.2)
    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Discount Rate Applied (%)")
    ax.set_ylabel("Average Profit Margin (%)")
    ax.set_title("Empirical Association: Discount Rate vs. Average Profit Margin", weight="bold", pad=12)

    for _, row in disc_rate_summary.iterrows():
        x_val = row["Discount"] * 100
        y_val = row["Avg_Profit_Margin"] * 100
        ax.annotate(f"{y_val:.1f}%", xy=(x_val, y_val), xytext=(0, 6 if y_val >= 0 else -12),
                    textcoords="offset points", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, "05_discount_vs_profit_margin.png"))
    plt.close()

    # Chart 6: Customer Segment and Shipping Mode Distributions
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    seg_summary_sorted = seg_summary.sort_values(by="Total_Sales", ascending=False)
    ax1.bar(seg_summary_sorted["Segment"], seg_summary_sorted["Total_Sales"] / 1000, color="#3182bd")
    ax1.set_ylabel("Sales ($ in Thousands)")
    ax1.set_title("Sales by Customer Segment", weight="bold")
    for bar in ax1.patches:
        h = bar.get_height()
        ax1.annotate(f"${h:.1f}k", (bar.get_x() + bar.get_width()/2, h), textcoords="offset points",
                     xytext=(0, 3), ha="center", fontsize=9)

    ship_summary = df.groupby("Ship Mode").agg(
        Transaction_Count=("Sales", "count")
    ).reset_index().sort_values(by="Transaction_Count", ascending=False)
    ax2.bar(ship_summary["Ship Mode"], ship_summary["Transaction_Count"], color="#756bb1")
    ax2.set_ylabel("Transaction Count")
    ax2.set_title("Transaction Volume by Ship Mode", weight="bold")
    ax2.tick_params(axis="x", rotation=15)
    for bar in ax2.patches:
        h = bar.get_height()
        ax2.annotate(f"{int(h):,}", (bar.get_x() + bar.get_width()/2, h), textcoords="offset points",
                     xytext=(0, 3), ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, "06_segment_and_ship_mode.png"))
    plt.close()
    print("[OK] Generated 6 visuals and 5 summary CSVs.")

if __name__ == "__main__":
    generate_eda()
