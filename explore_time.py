import pandas as pd

# ==================================
# 1. Đọc dữ liệu
# ==================================
df = pd.read_csv("data\SampleSuperstore.csv")

# ==================================
# 2. Chuyển đổi kiểu dữ liệu ngày tháng
# Dataset mới sử dụng định dạng MM/DD/YYYY
# ==================================
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y"
)

# ==================================
# 3. Tạo cột Year và YearMonth
# ==================================
df["Year"] = df["Order Date"].dt.year
df["YearMonth"] = df["Order Date"].dt.to_period("M")

# ==================================
# 4. Doanh thu theo tháng
# ==================================
monthly_sales = (
    df.groupby("YearMonth", as_index=False)["Sales"]
      .sum()
)

print("\n========== DOANH THU THEO THÁNG ==========")
print(monthly_sales.head(10))
print(monthly_sales.tail(10))

# ==================================
# 5. Tháng doanh thu cao nhất
# ==================================
best_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax()
]

print("\n========== THÁNG DOANH THU CAO NHẤT ==========")
print(best_month)

# ==================================
# 6. Tháng doanh thu thấp nhất
# ==================================
worst_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmin()
]

print("\n========== THÁNG DOANH THU THẤP NHẤT ==========")
print(worst_month)

# ==================================
# 7. Doanh thu theo năm
# ==================================
yearly_sales = (
    df.groupby("Year", as_index=False)["Sales"]
      .sum()
)

print("\n========== DOANH THU THEO NĂM ==========")
print(yearly_sales)

print(df.head())
print(df["Order Date"].head())
print(df.columns.tolist())