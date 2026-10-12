import os
import sys

# ======================================================
# XÁC ĐỊNH THƯ MỤC GỐC CỦA PROJECT
# ======================================================

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, project_root)

# ======================================================
# IMPORT THƯ VIỆN
# ======================================================

import streamlit as st
import pandas as pd

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.analysis import (
    get_top_products,
    get_top_subcategory,
    get_quantity_by_category,
    get_quantity_by_region,
    get_quantity_by_subcategory,
    get_bottom_products,
    get_bottom_profit_products
)

from src.visualization import (
    top_products_chart,
    top_subcategory_chart,
    quantity_by_category_chart,
    quantity_by_region_chart,
    quantity_by_subcategory_chart,
    bottom_products_chart,
    bottom_profit_products_chart
)

# ======================================================
# CẤU HÌNH TRANG
# ======================================================

st.set_page_config(
    page_title="Phân tích Sản phẩm",
    page_icon="📦",
    layout="wide"
)

# ======================================================
# TIÊU ĐỀ
# ======================================================

st.title("📦 PHÂN TÍCH HIỆU QUẢ SẢN PHẨM")

st.markdown(
    """
    Trang phân tích tập trung đánh giá **doanh số, số lượng bán,
    lợi nhuận và mức độ đóng góp của từng sản phẩm, danh mục
    và danh mục phụ** trong hoạt động kinh doanh.
    
    Các kết quả được sử dụng để xác định sản phẩm bán chạy,
    sản phẩm có hiệu quả thấp và hỗ trợ nhà quản lý đưa ra
    quyết định về hàng hóa, tồn kho và chiến lược kinh doanh.
    """
)

st.markdown("---")

# ======================================================
# TẢI DỮ LIỆU
# ======================================================

df = load_data(r"data\SampleSuperstore.csv")
df = clean_data(df)

# ======================================================
# BỘ LỌC SIDEBAR
# ======================================================

st.sidebar.title("🔎 Bộ lọc Dashboard")

st.sidebar.caption(
    "Các biểu đồ và chỉ số sẽ được cập nhật theo bộ lọc."
)

years = ["Tất cả"] + sorted(
    df["Year"].dropna().unique().tolist()
)

regions = ["Tất cả"] + sorted(
    df["Region"].dropna().unique().tolist()
)

categories = ["Tất cả"] + sorted(
    df["Category"].dropna().unique().tolist()
)

segments = ["Tất cả"] + sorted(
    df["Segment"].dropna().unique().tolist()
)

selected_year = st.sidebar.selectbox(
    "📅 Năm",
    years
)

selected_region = st.sidebar.selectbox(
    "🌍 Khu vực",
    regions
)

selected_category = st.sidebar.selectbox(
    "📂 Danh mục",
    categories
)

selected_segment = st.sidebar.selectbox(
    "👥 Phân khúc khách hàng",
    segments
)

# ======================================================
# ÁP DỤNG BỘ LỌC
# ======================================================

df = apply_filters(
    df,
    year="All" if selected_year == "Tất cả" else selected_year,
    region="All" if selected_region == "Tất cả" else selected_region,
    category="All" if selected_category == "Tất cả" else selected_category,
    segment="All" if selected_segment == "Tất cả" else selected_segment
)

# ======================================================
# KIỂM TRA DỮ LIỆU
# ======================================================

if df.empty:

    st.warning(
        """
        ⚠️ Không có dữ liệu phù hợp với các điều kiện lọc hiện tại.
        
        Vui lòng thay đổi bộ lọc để tiếp tục phân tích.
        """
    )

    st.stop()

# ======================================================
# KPI SẢN PHẨM
# ======================================================

st.subheader("📌 Chỉ số hiệu suất sản phẩm")

# Tổng doanh thu
total_sales = df["Sales"].sum()

# Tổng lợi nhuận
total_profit = df["Profit"].sum()

# Tổng số lượng
total_quantity = df["Quantity"].sum()

# Số sản phẩm khác nhau
total_products = df["Product Name"].nunique()

# Giá trị doanh thu trung bình / sản phẩm
avg_sales_product = (
    total_sales / total_products
    if total_products > 0
    else 0
)

# Biên lợi nhuận
profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Tổng doanh thu",
        f"${total_sales:,.2f}"
    )

with col2:

    st.metric(
        "📈 Tổng lợi nhuận",
        f"${total_profit:,.2f}"
    )

with col3:

    st.metric(
        "📦 Số lượng bán",
        f"{total_quantity:,.0f}"
    )

with col4:

    st.metric(
        "🛍 Số sản phẩm",
        f"{total_products:,}"
    )

col5, col6 = st.columns(2)

with col5:

    st.metric(
        "💵 Doanh thu TB / sản phẩm",
        f"${avg_sales_product:,.2f}"
    )

with col6:

    st.metric(
        "📊 Biên lợi nhuận",
        f"{profit_margin:.2f}%"
    )

st.markdown("---")

# ======================================================
# PHÂN TÍCH TOP SẢN PHẨM
# ======================================================

st.subheader("🏆 Nhóm sản phẩm có hiệu quả cao")

st.markdown(
    """
    Phân tích nhóm sản phẩm dẫn đầu giúp xác định những mặt hàng
    đóng góp lớn vào doanh số và là cơ sở để ưu tiên nguồn lực,
    quản lý tồn kho và xây dựng chiến lược bán hàng.
    """
)

top_products = get_top_products(df)

st.plotly_chart(
    top_products_chart(top_products),
    use_container_width=True
)

# ======================================================
# TẠO BẢNG TOP SẢN PHẨM
# ======================================================

product_sales = (
    df.groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
)

top10_products = product_sales.head(10).copy()

top10_products["Tỷ trọng doanh thu (%)"] = (
    top10_products["Sales"] / total_sales * 100
)

top10_products = top10_products[
    [
        "Product Name",
        "Sales",
        "Profit",
        "Quantity",
        "Tỷ trọng doanh thu (%)"
    ]
]

with st.expander("📄 Xem chi tiết Top 10 sản phẩm"):

    st.dataframe(
        top10_products,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# ======================================================
# DANH MỤC & DANH MỤC PHỤ
# ======================================================

st.subheader("📊 Phân tích cơ cấu sản phẩm")

st.markdown(
    """
    Việc phân tích theo danh mục và danh mục phụ giúp đánh giá
    cơ cấu hàng hóa, xác định nhóm sản phẩm có nhu cầu cao
    và nhận diện sự khác biệt về hiệu quả giữa các nhóm.
    """
)

top_subcategory = get_top_subcategory(df)

quantity_category = get_quantity_by_category(df)

quantity_subcategory = get_quantity_by_subcategory(df)

left, right = st.columns(2)

with left:

    st.markdown("### 📂 Số lượng sản phẩm theo Danh mục")

    st.plotly_chart(
        quantity_by_category_chart(quantity_category),
        use_container_width=True
    )

with right:

    st.markdown("### 📦 Danh mục phụ bán chạy")

    st.plotly_chart(
        top_subcategory_chart(top_subcategory),
        use_container_width=True
    )

st.markdown("---")

# ======================================================
# PHÂN TÍCH THEO KHU VỰC
# ======================================================

st.subheader("🌍 Phân bố sản lượng theo Khu vực")

st.markdown(
    """
    Phân tích khu vực giúp xác định thị trường có nhu cầu sản phẩm
    cao, từ đó hỗ trợ doanh nghiệp điều chỉnh phân bổ hàng hóa
    và nguồn lực bán hàng theo từng khu vực.
    """
)

quantity_region = get_quantity_by_region(df)

st.plotly_chart(
    quantity_by_region_chart(quantity_region),
    use_container_width=True
)

st.markdown("---")

# ======================================================
# PHÂN TÍCH DANH MỤC PHỤ
# ======================================================

st.subheader("📦 Chi tiết sản lượng theo Danh mục phụ")

st.plotly_chart(
    quantity_by_subcategory_chart(quantity_subcategory),
    use_container_width=True
)

st.markdown("---")

# ======================================================
# PHÂN TÍCH SẢN PHẨM YẾU
# ======================================================

st.subheader("⚠️ Nhận diện sản phẩm có hiệu quả thấp")

st.markdown(
    """
    Bên cạnh việc xác định sản phẩm bán chạy, hệ thống cũng phân tích
    nhóm sản phẩm có doanh số và lợi nhuận thấp. Đây là cơ sở để
    doanh nghiệp xem xét chính sách giá, khuyến mãi, tồn kho hoặc
    khả năng tiếp tục kinh doanh sản phẩm.
    """
)

bottom_products = get_bottom_products(df)

bottom_profit_products = get_bottom_profit_products(df)

left, right = st.columns(2)

with left:

    st.markdown("### 📉 10 sản phẩm có doanh số thấp nhất")

    st.plotly_chart(
        bottom_products_chart(bottom_products),
        use_container_width=True
    )

with right:

    st.markdown("### ❌ 10 sản phẩm có lợi nhuận thấp nhất")

    st.plotly_chart(
        bottom_profit_products_chart(bottom_profit_products),
        use_container_width=True
    )

st.markdown("---")

# ======================================================
# PHÂN TÍCH SẢN PHẨM LỢI NHUẬN ÂM
# ======================================================

st.subheader("🔴 Sản phẩm có dấu hiệu rủi ro về lợi nhuận")

negative_profit = (
    df.groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
)

negative_profit = negative_profit[
    negative_profit["Profit"] < 0
].sort_values(
    "Profit",
    ascending=True
)

if not negative_profit.empty:

    negative_count = len(negative_profit)

    negative_profit_total = negative_profit["Profit"].sum()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "⚠️ Số sản phẩm có lợi nhuận âm",
            f"{negative_count:,}"
        )

    with col2:

        st.metric(
            "💸 Tổng lợi nhuận âm",
            f"${negative_profit_total:,.2f}"
        )

    with st.expander("📄 Xem danh sách sản phẩm có lợi nhuận âm"):

        st.dataframe(
            negative_profit.head(20),
            use_container_width=True,
            hide_index=True
        )

else:

    st.success(
        "✅ Không phát hiện sản phẩm có lợi nhuận âm trong phạm vi dữ liệu đang lọc."
    )

st.markdown("---")

# ======================================================
# NHẬN ĐỊNH TỰ ĐỘNG
# ======================================================

st.subheader("💡 Nhận định từ dữ liệu")

# Sản phẩm đứng đầu
best_product = product_sales.iloc[0]

# Sản phẩm lợi nhuận cao nhất
product_profit = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

best_profit_product = product_profit.index[0]
best_profit_value = product_profit.iloc[0]

# Danh mục có doanh thu cao nhất
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

best_category = category_sales.index[0]
best_category_sales = category_sales.iloc[0]

# Khu vực có sản lượng cao nhất
region_quantity = (
    df.groupby("Region")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

best_quantity_region = region_quantity.index[0]
best_quantity_value = region_quantity.iloc[0]

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"""
        **🏆 Sản phẩm dẫn đầu về doanh thu**

        **{best_product['Product Name']}**

        Doanh thu: **${best_product['Sales']:,.2f}**

        Sản phẩm này hiện là mặt hàng có doanh thu cao nhất
        trong phạm vi dữ liệu sau khi áp dụng bộ lọc.
        """
    )

with col2:

    st.success(
        f"""
        **📈 Sản phẩm dẫn đầu về lợi nhuận**

        **{best_profit_product}**

        Lợi nhuận: **${best_profit_value:,.2f}**

        Đây là sản phẩm có mức đóng góp lợi nhuận cao nhất
        trong phạm vi dữ liệu đang phân tích.
        """
    )

col3, col4 = st.columns(2)

with col3:

    st.warning(
        f"""
        **📂 Danh mục có doanh thu cao nhất**

        **{best_category}**

        Doanh thu: **${best_category_sales:,.2f}**

        Danh mục này cần được ưu tiên theo dõi về doanh số,
        tồn kho và hiệu quả kinh doanh.
        """
    )

with col4:

    st.info(
        f"""
        **🌍 Khu vực có sản lượng cao nhất**

        **{best_quantity_region}**

        Số lượng bán: **{best_quantity_value:,.0f}**

        Đây là khu vực có nhu cầu sản phẩm cao nhất
        trong phạm vi dữ liệu hiện tại.
        """
    )

st.markdown("---")

# ======================================================
# ĐỀ XUẤT QUẢN TRỊ
# ======================================================

st.subheader("🎯 Đề xuất quản trị")

recommendations = []

if best_product["Sales"] > 0:

    recommendations.append(
        f"Ưu tiên duy trì nguồn cung và tồn kho cho sản phẩm "
        f"**{best_product['Product Name']}**, do đây là sản phẩm "
        f"dẫn đầu về doanh thu."
    )

if not negative_profit.empty:

    recommendations.append(
        f"Cần rà soát **{negative_count} sản phẩm có lợi nhuận âm**, "
        f"đặc biệt là các sản phẩm có mức lỗ lớn, để đánh giá lại "
        f"giá bán, chiết khấu và chi phí liên quan."
    )

recommendations.append(
    f"Tập trung theo dõi danh mục **{best_category}**, "
    f"là danh mục đang tạo ra doanh thu cao nhất."
)

recommendations.append(
    f"Ưu tiên phân bổ hàng hóa phù hợp cho khu vực "
    f"**{best_quantity_region}**, nơi có sản lượng bán cao nhất."
)

recommendations.append(
    "Kết hợp đồng thời chỉ tiêu doanh thu và lợi nhuận khi đánh giá "
    "sản phẩm, tránh chỉ tập trung vào các mặt hàng có doanh số cao "
    "nhưng hiệu quả lợi nhuận thấp."
)

for i, recommendation in enumerate(
    recommendations,
    start=1
):

    st.write(
        f"**{i}.** {recommendation}"
    )

st.markdown("---")

# ======================================================
# BẢNG PHÂN TÍCH SẢN PHẨM
# ======================================================

st.subheader("📄 Bảng dữ liệu phân tích sản phẩm")

st.caption(
    "Bảng dưới đây tổng hợp doanh thu, lợi nhuận và số lượng bán "
    "theo từng sản phẩm trong phạm vi bộ lọc hiện tại."
)

product_detail = (
    df.groupby("Product Name", as_index=False)
    .agg(
        Doanh_thu=("Sales", "sum"),
        Loi_nhuan=("Profit", "sum"),
        So_luong_ban=("Quantity", "sum")
    )
    .sort_values(
        "Doanh_thu",
        ascending=False
    )
)

product_detail["Ty_trong_doanh_thu"] = (
    product_detail["Doanh_thu"]
    / total_sales
    * 100
)

product_detail["Bien_loi_nhuan"] = (
    product_detail["Loi_nhuan"]
    / product_detail["Doanh_thu"]
    * 100
).fillna(0)

product_detail = product_detail.rename(
    columns={
        "Product Name": "Sản phẩm",
        "Doanh_thu": "Doanh thu",
        "Loi_nhuan": "Lợi nhuận",
        "So_luong_ban": "Số lượng bán",
        "Ty_trong_doanh_thu": "Tỷ trọng doanh thu (%)",
        "Bien_loi_nhuan": "Biên lợi nhuận (%)"
    }
)

st.dataframe(
    product_detail,
    use_container_width=True,
    hide_index=True
)

