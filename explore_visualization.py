import pandas as pd
import plotly.express as px

# ==========================
# Đọc dữ liệu
# ==========================
df = pd.read_csv("data\SampleSuperstore.csv")

# ==========================
# Chuyển đổi ngày
# ==========================
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y"
)

# ==========================
# Doanh thu theo tháng
# ==========================
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("YearMonth", as_index=False)["Sales"]
      .sum()
)

fig = px.line(
    monthly_sales,
    x="YearMonth",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True,
    labels={
        "YearMonth": "Month",
        "Sales": "Sales ($)"
    }
)

fig.show()

# ==========================
# Doanh thu theo khu vực
# ==========================
sales_by_region = (
    df.groupby("Region", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

fig = px.bar(
    sales_by_region,
    x="Region",
    y="Sales",
    title="Sales by Region",
    color="Sales",
    text_auto=".2s"
)

fig.show()

# ==========================
# Doanh thu theo Category
# ==========================
sales_by_category = (
    df.groupby("Category", as_index=False)["Sales"]
      .sum()
)

fig = px.pie(
    sales_by_category,
    names="Category",
    values="Sales",
    title="Sales by Category",
    hole=0.4
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.show()