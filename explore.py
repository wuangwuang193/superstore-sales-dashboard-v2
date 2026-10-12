import pandas as pd

# ==================================
# 1. Đọc dữ liệu
# ==================================
df = pd.read_csv(r"data\SampleSuperstore.csv")

# ==================================
# 2. Hiển thị dữ liệu mẫu
# ==================================
print("\n========== 5 DÒNG ĐẦU TIÊN ==========")
print(df.head())

# ==================================
# 3. Thông tin tổng quan
# ==================================
print("\n========== THÔNG TIN DATASET ==========")
df.info()

print("\n========== DANH SÁCH CỘT ==========")
print(df.columns.tolist())

# ==================================
# 4. Kiểm tra giá trị thiếu
# ==================================
print("\n========== GIÁ TRỊ THIẾU ==========")
print(df.isnull().sum())

# ==================================
# 5. Kiểm tra dữ liệu trùng
# ==================================
print("\n========== DỮ LIỆU TRÙNG ==========")
print("Số dòng trùng:", df.duplicated().sum())

# ==================================
# 6. Kiểu dữ liệu ban đầu
# ==================================
print("\n========== KIỂU DỮ LIỆU ==========")
print(df.dtypes)

# ==================================
# 7. Chuyển đổi ngày tháng
# Dataset mới sử dụng định dạng MM/DD/YYYY
# ==================================
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%m/%d/%Y"
)

print("\n========== SAU KHI CHUYỂN ĐỔI NGÀY ==========")
print(df[["Order Date", "Ship Date"]].dtypes)

# ==================================
# 8. Phạm vi thời gian
# ==================================
print("\n========== PHẠM VI THỜI GIAN ==========")
print("Ngày đầu tiên :", df["Order Date"].min())
print("Ngày cuối cùng:", df["Order Date"].max())

# ==================================
# 9. KPI TỔNG QUAN
# ==================================
revenue = df["Sales"].sum()
profit = df["Profit"].sum()
quantity = df["Quantity"].sum()
orders = df["Order ID"].nunique()
customers = df["Customer ID"].nunique()
products = df["Product ID"].nunique()

print("\n========== KPI TỔNG QUAN ==========")
print(f"Tổng doanh thu      : {revenue:,.2f}")
print(f"Tổng lợi nhuận      : {profit:,.2f}")
print(f"Tổng số lượng bán   : {quantity:,}")
print(f"Số đơn hàng         : {orders:,}")
print(f"Số khách hàng       : {customers:,}")
print(f"Số sản phẩm         : {products:,}")

# ==================================
# 10. Thống kê mô tả
# ==================================
print("\n========== THỐNG KÊ DỮ LIỆU ==========")
print(df[["Sales", "Profit", "Quantity", "Discount"]].describe())

# ==================================
# 11. Top 5 đơn hàng doanh thu cao nhất
# ==================================
print("\n========== TOP 5 ĐƠN HÀNG DOANH THU CAO NHẤT ==========")
print(
    df[["Order ID", "Customer Name", "Sales"]]
    .sort_values(by="Sales", ascending=False)
    .head()
)

# ==================================
# 12. Top 5 đơn hàng lợi nhuận cao nhất
# ==================================
print("\n========== TOP 5 ĐƠN HÀNG LỢI NHUẬN CAO NHẤT ==========")
print(
    df[["Order ID", "Customer Name", "Profit"]]
    .sort_values(by="Profit", ascending=False)
    .head()
)