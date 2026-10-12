import os
import sys

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, project_root)

import streamlit as st

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.kpi import (
    get_total_customers,
    get_total_sales,
    get_total_orders
)

from src.analysis import (
    get_top_customers,
    get_sales_by_segment,
    get_customer_count_by_segment
)

from src.visualization import (
    top_customers_chart,
    sales_by_segment_chart,
    customer_segment_chart
)


# ==========================================================
# CẤU HÌNH TRANG
# ==========================================================

st.set_page_config(
    page_title="Phân tích Khách hàng",
    page_icon="👥",
    layout="wide"
)


# ==========================================================
# TẢI DỮ LIỆU
# ==========================================================

df = load_data(r"data\SampleSuperstore.csv")
df = clean_data(df)


# ==========================================================
# TIÊU ĐỀ
# ==========================================================

st.title("👥 Dashboard Phân tích Khách hàng")

st.markdown(
    """
    Trang phân tích tập trung đánh giá đặc điểm khách hàng,
    mức đóng góp doanh thu và cơ cấu theo từng phân khúc.
    Kết quả phân tích được sử dụng để xác định nhóm khách hàng
    có giá trị và hỗ trợ doanh nghiệp xây dựng chính sách chăm sóc
    khách hàng phù hợp.
    """
)

st.markdown("---")


# ==========================================================
# BỘ LỌC SIDEBAR
# ==========================================================

st.sidebar.header("🔎 Bộ lọc Dashboard")

years = ["Tất cả"] + sorted(
    df["Year"].unique().tolist()
)

regions = ["Tất cả"] + sorted(
    df["Region"].unique().tolist()
)

categories = ["Tất cả"] + sorted(
    df["Category"].unique().tolist()
)

segments = ["Tất cả"] + sorted(
    df["Segment"].unique().tolist()
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
    "📦 Danh mục",
    categories
)

selected_segment = st.sidebar.selectbox(
    "👥 Phân khúc",
    segments
)


# ==========================================================
# CHUYỂN ĐỔI GIÁ TRỊ BỘ LỌC
# ==========================================================

filter_year = (
    "All"
    if selected_year == "Tất cả"
    else selected_year
)

filter_region = (
    "All"
    if selected_region == "Tất cả"
    else selected_region
)

filter_category = (
    "All"
    if selected_category == "Tất cả"
    else selected_category
)

filter_segment = (
    "All"
    if selected_segment == "Tất cả"
    else selected_segment
)


# ==========================================================
# ÁP DỤNG BỘ LỌC
# ==========================================================

df = apply_filters(
    df,
    year=filter_year,
    region=filter_region,
    category=filter_category,
    segment=filter_segment
)


# ==========================================================
# KPI KHÁCH HÀNG
# ==========================================================

st.subheader("📌 Chỉ số tổng quan khách hàng")


# Sử dụng cùng hàm KPI với trang Tổng quan
# để đảm bảo số liệu thống nhất giữa các trang.

total_customers = get_total_customers(df)

total_sales = get_total_sales(df)

total_orders = get_total_orders(df)

total_quantity = df["Quantity"].sum()


if total_customers > 0:

    average_sales_customer = (
        total_sales / total_customers
    )

else:

    average_sales_customer = 0


# ==========================================================
# HIỂN THỊ KPI
# ==========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="👥 Tổng khách hàng",
        value=f"{total_customers:,}"
    )


with col2:

    st.metric(
        label="💰 Tổng doanh thu",
        value=f"${total_sales:,.2f}"
    )


with col3:

    st.metric(
        label="🛒 Tổng đơn hàng",
        value=f"{total_orders:,}"
    )


with col4:

    st.metric(
        label="📊 Doanh thu / khách hàng",
        value=f"${average_sales_customer:,.2f}"
    )


st.markdown("---")


# ==========================================================
# PHÂN TÍCH DỮ LIỆU
# ==========================================================

top_customers = get_top_customers(df)

sales_segment = get_sales_by_segment(df)

customer_segment = get_customer_count_by_segment(df)


# ==========================================================
# TOP 10 KHÁCH HÀNG
# ==========================================================

st.subheader("🏆 Top 10 Khách hàng theo Doanh thu")

st.markdown(
    """
    Biểu đồ thể hiện doanh thu đóng góp của 10 khách hàng
    có giá trị doanh thu cao trong phạm vi dữ liệu được lựa chọn.
    """
)

st.plotly_chart(
    top_customers_chart(top_customers),
    use_container_width=True
)


# ==========================================================
# PHÂN TÍCH PHÂN KHÚC
# ==========================================================

st.markdown("---")

st.subheader("📊 Phân tích khách hàng theo Phân khúc")


left, right = st.columns(2)


# ----------------------------------------------------------
# DOANH THU THEO PHÂN KHÚC
# ----------------------------------------------------------

with left:

    st.markdown(
        "### 💰 Doanh thu theo Phân khúc"
    )

    st.plotly_chart(
        sales_by_segment_chart(sales_segment),
        use_container_width=True
    )


# ----------------------------------------------------------
# SỐ LƯỢNG KHÁCH HÀNG THEO PHÂN KHÚC
# ----------------------------------------------------------

with right:

    st.markdown(
        "### 👥 Số lượng Khách hàng theo Phân khúc"
    )

    st.plotly_chart(
        customer_segment_chart(customer_segment),
        use_container_width=True
    )


# ==========================================================
# PHÂN TÍCH MỨC ĐÓNG GÓP CỦA TOP 10 KHÁCH HÀNG
# ==========================================================

st.markdown("---")

st.subheader("📈 Mức đóng góp của nhóm khách hàng trọng điểm")


if len(top_customers) > 0:

    top_customer_sales = top_customers["Sales"].sum()

else:

    top_customer_sales = 0


if total_sales != 0:

    top_customer_ratio = (
        top_customer_sales
        / total_sales
        * 100
    )

else:

    top_customer_ratio = 0


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "💰 Doanh thu Top 10 khách hàng",
        f"${top_customer_sales:,.2f}"
    )


with col2:

    st.metric(
        "📊 Tỷ trọng doanh thu",
        f"{top_customer_ratio:.2f}%"
    )


st.info(
    f"""
    Nhóm Top 10 khách hàng tạo ra doanh thu khoảng
    **${top_customer_sales:,.2f}**, tương đương
    **{top_customer_ratio:.2f}%** tổng doanh thu trong phạm vi
    dữ liệu đang được phân tích.

    Chỉ số này cho phép đánh giá mức độ tập trung doanh thu
    vào nhóm khách hàng có giá trị cao, từ đó hỗ trợ doanh nghiệp
    xác định nhóm khách hàng cần ưu tiên duy trì và chăm sóc.
    """
)


# ==========================================================
# PHÂN TÍCH PHÂN KHÚC CÓ ĐÓNG GÓP CAO
# ==========================================================

st.markdown("---")

st.subheader("🔎 Nhận định về Cơ cấu Khách hàng")


if len(sales_segment) > 0:

    # Tìm phân khúc có doanh thu cao nhất
    best_segment = sales_segment.sort_values(
        "Sales",
        ascending=False
    ).iloc[0]

    best_segment_name = best_segment["Segment"]

    best_segment_sales = best_segment["Sales"]


    if total_sales != 0:

        best_segment_ratio = (
            best_segment_sales
            / total_sales
            * 100
        )

    else:

        best_segment_ratio = 0


    st.success(
        f"""
        Phân khúc **{best_segment_name}** đang đóng góp khoảng
        **${best_segment_sales:,.2f}** doanh thu,
        tương đương **{best_segment_ratio:.2f}%** tổng doanh thu.

        Kết quả cho thấy đây là nhóm khách hàng có vai trò đáng kể
        đối với kết quả kinh doanh trong phạm vi dữ liệu đang phân tích.
        Doanh nghiệp có thể ưu tiên duy trì quan hệ với nhóm khách hàng
        này, đồng thời nghiên cứu đặc điểm và nhu cầu của họ để xây dựng
        các chính sách bán hàng phù hợp.
        """
    )


# ==========================================================
# THÔNG TIN PHÂN TÍCH
# ==========================================================

st.markdown("---")

st.subheader("💡 Một số chỉ số hỗ trợ phân tích")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📦 Tổng sản phẩm bán ra",
        f"{total_quantity:,}"
    )


with col2:

    if total_orders > 0:

        average_order_value = (
            total_sales / total_orders
        )

    else:

        average_order_value = 0


    st.metric(
        "🛒 Giá trị đơn hàng TB",
        f"${average_order_value:,.2f}"
    )


with col3:

    if total_customers > 0:

        orders_per_customer = (
            total_orders / total_customers
        )

    else:

        orders_per_customer = 0


    st.metric(
        "🔄 Đơn hàng / khách hàng",
        f"{orders_per_customer:.2f}"
    )


# ==========================================================
# XEM DỮ LIỆU
# ==========================================================

st.markdown("---")

st.subheader("📄 Tập dữ liệu Khách hàng")

st.markdown(
    """
    Bảng dữ liệu dưới đây thể hiện tập dữ liệu sau khi đã
    thực hiện làm sạch và áp dụng các điều kiện lọc trên Dashboard.
    """
)

st.dataframe(
    df,
    use_container_width=True,
    height=450
)


