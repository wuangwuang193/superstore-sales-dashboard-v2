import os
import sys

# ==========================================================
# PROJECT ROOT
# ==========================================================

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, project_root)

# ==========================================================
# LIBRARIES
# ==========================================================

import streamlit as st
import pandas as pd

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.analysis import (
    get_monthly_sales,
    get_sales_growth,
    get_sales_by_region,
    get_sales_by_category,
    get_sales_by_state,
    get_top_subcategory
)

from src.visualization import (
    monthly_sales_chart,
    sales_growth_chart,
    sales_by_region_chart,
    sales_by_category_chart,
    sales_by_state_chart,
    top_subcategory_chart
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Phân tích Doanh thu | Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* =========================
       MAIN
    ========================= */

    .main {
        padding-top: 1rem;
    }

    /* =========================
       TITLE
    ========================= */

    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .dashboard-description {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 20px;
    }

    /* =========================
       KPI CARD
    ========================= */

    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px 20px;
        min-height: 125px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .kpi-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 27px;
        font-weight: 700;
        color: #111827;
    }

    .kpi-sub {
        font-size: 13px;
        color: #6b7280;
        margin-top: 5px;
    }

    /* =========================
       SECTION
    ========================= */

    .section-title {
        font-size: 23px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* =========================
       INSIGHT
    ========================= */

    .insight-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: #f9fafb;
        margin-bottom: 10px;
    }

    .insight-title {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 6px;
    }

    .insight-text {
        font-size: 14px;
        color: #4b5563;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="dashboard-title">📈 Phân tích Doanh thu</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="dashboard-description">
    Phân tích toàn diện tình hình doanh thu theo thời gian,
    khu vực địa lý, danh mục sản phẩm và phân khúc khách hàng.
    Hệ thống hỗ trợ nhà quản lý nhận diện xu hướng và đưa ra
    quyết định dựa trên dữ liệu.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data(r"data\SampleSuperstore.csv")
df = clean_data(df)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("🔎 Bộ lọc Dashboard")

st.sidebar.caption(
    "Lựa chọn điều kiện để cập nhật toàn bộ kết quả phân tích."
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
    "🛍 Danh mục",
    categories
)

selected_segment = st.sidebar.selectbox(
    "👥 Phân khúc khách hàng",
    segments
)

# ==========================================================
# FILTER
# ==========================================================

df_filtered = apply_filters(
    df,
    year="All" if selected_year == "Tất cả" else selected_year,
    region="All" if selected_region == "Tất cả" else selected_region,
    category="All" if selected_category == "Tất cả" else selected_category,
    segment="All" if selected_segment == "Tất cả" else selected_segment
)

if df_filtered.empty:

    st.warning(
        "⚠️ Không có dữ liệu phù hợp với bộ lọc hiện tại."
    )

    st.stop()

# ==========================================================
# KPI
# ==========================================================

total_sales = df_filtered["Sales"].sum()

total_profit = (
    df_filtered["Profit"].sum()
    if "Profit" in df_filtered.columns
    else 0
)

total_orders = (
    df_filtered["Order ID"].nunique()
    if "Order ID" in df_filtered.columns
    else len(df_filtered)
)

total_customers = (
    df_filtered["Customer ID"].nunique()
    if "Customer ID" in df_filtered.columns
    else df_filtered["Customer Name"].nunique()
)

total_products = df_filtered["Product Name"].nunique()

total_quantity = df_filtered["Quantity"].sum()

# ==========================================================
# DERIVED KPI
# ==========================================================

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

avg_order_value = (
    total_sales / total_orders
    if total_orders != 0
    else 0
)

# ==========================================================
# KPI HEADER
# ==========================================================

st.markdown(
    '<div class="section-title">📌 Tổng quan hiệu suất</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Các chỉ số chính phản ánh quy mô và hiệu quả kinh doanh '
    'trong phạm vi dữ liệu đang được lựa chọn.'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================================
# KPI ROW 1
# ==========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Tổng doanh thu</div>
            <div class="kpi-value">${total_sales:,.2f}</div>
            <div class="kpi-sub">Tổng giá trị bán hàng</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💵 Tổng lợi nhuận</div>
            <div class="kpi-value">${total_profit:,.2f}</div>
            <div class="kpi-sub">
                Biên lợi nhuận: {profit_margin:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🧾 Tổng đơn hàng</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-sub">
                Giá trị TB/đơn: ${avg_order_value:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ==========================================================
# KPI ROW 2
# ==========================================================

col4, col5, col6 = st.columns(3)

with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Khách hàng</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-sub">Khách hàng có giao dịch</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛍 Sản phẩm</div>
            <div class="kpi-value">{total_products:,}</div>
            <div class="kpi-sub">Sản phẩm phát sinh giao dịch</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col6:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Số lượng bán</div>
            <div class="kpi-value">{total_quantity:,}</div>
            <div class="kpi-sub">Tổng số sản phẩm đã bán</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ==========================================================
# FILTER STATUS
# ==========================================================

with st.expander("🔎 Xem phạm vi dữ liệu đang phân tích"):

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.write("**📅 Năm**")
        st.write(selected_year)

    with f2:
        st.write("**🌍 Khu vực**")
        st.write(selected_region)

    with f3:
        st.write("**🛍 Danh mục**")
        st.write(selected_category)

    with f4:
        st.write("**👥 Phân khúc**")
        st.write(selected_segment)

st.divider()

# ==========================================================
# ANALYSIS
# ==========================================================

monthly_sales = get_monthly_sales(df_filtered)

sales_growth = get_sales_growth(df_filtered)

sales_region = get_sales_by_region(df_filtered)

sales_category = get_sales_by_category(df_filtered)

sales_state = get_sales_by_state(df_filtered)

top_subcategory = get_top_subcategory(df_filtered)

# ==========================================================
# TREND
# ==========================================================

st.markdown(
    '<div class="section-title">📈 Xu hướng doanh thu</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Theo dõi biến động doanh thu theo thời gian để nhận diện '
    'xu hướng tăng trưởng, suy giảm và các giai đoạn bất thường.'
    '</div>',
    unsafe_allow_html=True
)

st.plotly_chart(
    monthly_sales_chart(monthly_sales),
    use_container_width=True
)

# ==========================================================
# GROWTH
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Tăng trưởng doanh thu</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Đánh giá mức thay đổi doanh thu giữa các kỳ nhằm xác định '
    'giai đoạn tăng trưởng hoặc suy giảm.'
    '</div>',
    unsafe_allow_html=True
)

st.plotly_chart(
    sales_growth_chart(sales_growth),
    use_container_width=True
)

st.divider()

# ==========================================================
# REGION + CATEGORY
# ==========================================================

st.markdown(
    '<div class="section-title">🌍 Phân tích cơ cấu doanh thu</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### 🌍 Theo khu vực")

    st.plotly_chart(
        sales_by_region_chart(sales_region),
        use_container_width=True
    )

with col2:

    st.markdown("#### 🛍 Theo danh mục")

    st.plotly_chart(
        sales_by_category_chart(sales_category),
        use_container_width=True
    )

st.divider()

# ==========================================================
# DETAILED ANALYSIS
# ==========================================================

st.markdown(
    '<div class="section-title">🔍 Phân tích chi tiết</div>',
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(
    [
        "🏙 Phân tích theo Bang/Tỉnh",
        "📦 Phân tích Danh mục phụ"
    ]
)

with tab1:

    st.markdown(
        "Phân tích doanh thu theo từng bang/tỉnh "
        "nhằm xác định thị trường có đóng góp nổi bật."
    )

    st.plotly_chart(
        sales_by_state_chart(sales_state),
        use_container_width=True
    )

with tab2:

    st.markdown(
        "Phân tích danh mục phụ nhằm xác định "
        "những nhóm sản phẩm đóng góp doanh thu lớn."
    )

    st.plotly_chart(
        top_subcategory_chart(top_subcategory),
        use_container_width=True
    )

st.divider()

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.markdown(
    '<div class="section-title">💡 Thông tin chuyên sâu về kinh doanh</div>',
    unsafe_allow_html=True
)

region_analysis = (
    df_filtered
    .groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

category_analysis = (
    df_filtered
    .groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

if not region_analysis.empty:

    best_region = region_analysis.index[0]
    best_region_sales = region_analysis.iloc[0]

else:

    best_region = "Không xác định"
    best_region_sales = 0

if not category_analysis.empty:

    best_category = category_analysis.index[0]
    best_category_sales = category_analysis.iloc[0]

else:

    best_category = "Không xác định"
    best_category_sales = 0

insight1, insight2 = st.columns(2)

with insight1:

    st.markdown(
        f"""
        <div class="insight-box">

        <div class="insight-title">
        🌍 Khu vực dẫn đầu
        </div>

        <div class="insight-text">

        <b>{best_region}</b> đang là khu vực có doanh thu
        cao nhất với giá trị khoảng

        <b>${best_region_sales:,.2f}</b>.

        Đây là thị trường cần được tiếp tục theo dõi
        và khai thác nhằm duy trì mức đóng góp vào
        tổng doanh thu.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with insight2:

    st.markdown(
        f"""
        <div class="insight-box">

        <div class="insight-title">
        🛍 Danh mục dẫn đầu
        </div>

        <div class="insight-text">

        <b>{best_category}</b> đang đóng góp doanh thu
        cao nhất với giá trị khoảng

        <b>${best_category_sales:,.2f}</b>.

        Doanh nghiệp có thể tiếp tục phân tích sâu
        các sản phẩm thuộc nhóm này để xác định
        cơ hội tăng trưởng.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# SUMMARY
# ==========================================================

st.markdown("#### 📋 Tóm tắt kết quả")

summary_df = pd.DataFrame(
    {
        "Chỉ tiêu": [
            "Tổng doanh thu",
            "Tổng lợi nhuận",
            "Biên lợi nhuận",
            "Tổng đơn hàng",
            "Giá trị đơn hàng trung bình",
            "Tổng khách hàng",
            "Số sản phẩm",
            "Số lượng sản phẩm bán"
        ],

        "Giá trị": [
            f"${total_sales:,.2f}",
            f"${total_profit:,.2f}",
            f"{profit_margin:.2f}%",
            f"{total_orders:,}",
            f"${avg_order_value:,.2f}",
            f"{total_customers:,}",
            f"{total_products:,}",
            f"{total_quantity:,}"
        ]
    }
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# DOWNLOAD
# ==========================================================

st.divider()

st.subheader("📥 Xuất dữ liệu")

csv_data = df_filtered.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Tải dữ liệu sau khi lọc",
    data=csv_data,
    file_name="bao_cao_phan_tich_doanh_thu.csv",
    mime="text/csv"
)

# ==========================================================
# CONCLUSION
# ==========================================================

st.divider()
st.subheader("📝 Kết luận phân tích")

st.info(
    f"""
**Trong phạm vi dữ liệu hiện tại:**

- Tổng doanh thu đạt: **{total_sales:,.2f}**
- Tổng lợi nhuận đạt: **{total_profit:,.2f}**
- Biên lợi nhuận khoảng: **{profit_margin:.2f}%**


Các kết quả phân tích cung cấp cơ sở để doanh nghiệp đánh giá hiệu quả kinh doanh theo thời gian, xác định thị trường trọng điểm và nhận diện các nhóm sản phẩm có tiềm năng phát triển.
"""
)