import pandas as pd
# Đảm bảo các biến CATEGORY_MAP, SEGMENT_MAP... đã được định nghĩa trong src/translation.py
from src.translation import CATEGORY_MAP, SEGMENT_MAP, REGION_MAP, SUBCATEGORY_MAP

def clean_data(df):
    # 1. Chuyển đổi định dạng ngày tháng
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%m/%d/%Y",
        errors='coerce' # Tránh lỗi nếu có dữ liệu ngày không hợp lệ
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%m/%d/%Y",
        errors='coerce'
    )

    # 2. Trích xuất các thông tin thời gian
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Quarter"] = df["Order Date"].dt.quarter
    df["YearMonth"] = (
        df["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    # 3. DỊCH DỮ LIỆU (Sử dụng các dictionary từ src.translation)
    # Lưu ý: Các câu lệnh này phải thụt lề (tab) bằng với các câu lệnh trên
    df["Category"] = df["Category"].replace(CATEGORY_MAP)
    df["Segment"] = df["Segment"].replace(SEGMENT_MAP)
    df["Region"] = df["Region"].replace(REGION_MAP)
    df["Sub-Category"] = df["Sub-Category"].replace(SUBCATEGORY_MAP)

    return df