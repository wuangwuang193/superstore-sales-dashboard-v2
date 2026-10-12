import pandas as pd

# ===========================
# Đọc dữ liệu
# ===========================
df = pd.read_csv("data\SampleSuperstore.csv")

# Chuyển đổi ngày tháng
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y"
)

# ===========================
# Sales by Region
# ===========================
sales_by_region = (
    df.groupby("Region", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

print("\n===== SALES BY REGION =====")
print(sales_by_region)

# ===========================
# Sales by Category
# ===========================
sales_by_category = (
    df.groupby("Category", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

print("\n===== SALES BY CATEGORY =====")
print(sales_by_category)

# ===========================
# Sales by Sub-Category
# ===========================
sales_by_subcategory = (
    df.groupby("Sub-Category", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

print("\n===== TOP 10 SUB-CATEGORY =====")
print(sales_by_subcategory.head(10))

# ===========================
# Top Customers
# ===========================
top_customers = (
    df.groupby("Customer Name", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

print("\n===== TOP 10 CUSTOMERS =====")
print(top_customers.head(10))