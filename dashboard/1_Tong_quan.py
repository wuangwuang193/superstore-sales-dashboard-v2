import os
import sys

# ======================================================
# THIẾT LẬP ĐƯỜNG DẪN PROJECT
# ======================================================

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, project_root)

# ======================================================
# THƯ VIỆN
# ======================================================

import streamlit as st

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.kpi import (
    get_total_sales,
    get_total_profit,
    get_total_orders,
    get_total_customers,
    get_total_products,
    get_total_quantity,
    get_sales_growth_rate,
    get_profit_growth_rate
)

from src.analysis import (
    get_monthly_sales,
    get_sales_by_region,
    get_sales_by_category,
    get_best_region,
    get_best_category
)

from src.visualization import (
    monthly_sales_chart,
    sales_by_region_chart,
    sales_by_category_chart
)

from src.insights import (
    generate_insights,
    generate_recommendations
)


# ======================================================
# CẤU HÌNH TRANG
# ======================================================

st.set_page_config(
    page_title="Dashboard Phân tích Doanh thu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================================================
# CSS GIAO DIỆN
# ======================================================

st.markdown(
    """
    <style>

    /* Tiêu đề chính */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* KPI */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 15px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 27px;
        font-weight: 600;
    }

    /* Section */
    .section-title {
        font-size: 24px;
        font-weight: 650;
        color: #1f2937;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* Box */
    .info-box {
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .positive {
        color: #15803d;
        font-weight: 600;
    }

    .negative {
        color: #dc2626;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# TIÊU ĐỀ DASHBOARD
# ======================================================

st.markdown(
    '<div class="main-title">📊 Dashboard Phân tích Doanh thu</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
        Hệ thống trực quan hóa và phân tích hiệu quả kinh doanh
        dựa trên bộ dữ liệu Superstore.
    </div>
    """,
    unsafe_allow_html=True
)


# ======================================================
# TẢI VÀ LÀM SẠCH DỮ LIỆU
# ======================================================

df = load_data(r"data\SampleSuperstore.csv")
df = clean_data(df)


# ======================================================
# SIDEBAR - BỘ LỌC
# ======================================================

st.sidebar.markdown("## 🔎 Bộ lọc Dashboard")

st.sidebar.caption(
    "Sử dụng các bộ lọc để thay đổi phạm vi dữ liệu phân tích."
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


# ======================================================
# CHUYỂN ĐỔI GIÁ TRỊ BỘ LỌC
# ======================================================

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


# ======================================================
# ÁP DỤNG BỘ LỌC
# ======================================================

df = apply_filters(
    df,
    year=filter_year,
    region=filter_region,
    category=filter_category,
    segment=filter_segment
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
# THÔNG TIN PHẠM VI PHÂN TÍCH
# ======================================================

st.markdown(
    '<div class="section-title">📌 Phạm vi phân tích</div>',
    unsafe_allow_html=True
)

scope_col1, scope_col2, scope_col3, scope_col4 = st.columns(4)

with scope_col1:
    st.info(
        f"📅 **Năm:** {selected_year}"
    )

with scope_col2:
    st.info(
        f"🌍 **Khu vực:** {selected_region}"
    )

with scope_col3:
    st.info(
        f"🛍 **Danh mục:** {selected_category}"
    )

with scope_col4:
    st.info(
        f"👥 **Phân khúc:** {selected_segment}"
    )


st.markdown("---")


# ======================================================
# TÍNH TOÁN KPI
# ======================================================

total_sales = get_total_sales(df)
total_profit = get_total_profit(df)
total_orders = get_total_orders(df)
total_customers = get_total_customers(df)
total_products = get_total_products(df)
total_quantity = get_total_quantity(df)

sales_growth = get_sales_growth_rate(df)
profit_growth = get_profit_growth_rate(df)


# ======================================================
# TÍNH BIÊN LỢI NHUẬN
# ======================================================

if total_sales != 0:

    profit_margin = (
        total_profit / total_sales
    ) * 100

else:

    profit_margin = 0


# ======================================================
# KPI CHÍNH
# ======================================================

st.markdown(
    '<div class="section-title">📌 Chỉ số hiệu suất chính (KPI)</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="💰 Tổng doanh thu",
        value=f"${total_sales:,.2f}"
    )

with col2:

    st.metric(
        label="📈 Tổng lợi nhuận",
        value=f"${total_profit:,.2f}"
    )

with col3:

    st.metric(
        label="🛒 Số đơn hàng",
        value=f"{total_orders:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        label="👥 Tổng khách hàng",
        value=f"{total_customers:,}"
    )

with col5:

    st.metric(
        label="📦 Số sản phẩm",
        value=f"{total_products:,}"
    )

with col6:

    st.metric(
        label="📊 Số lượng sản phẩm đã bán",
        value=f"{total_quantity:,}"
    )


st.markdown("---")


# ======================================================
# KPI TĂNG TRƯỞNG
# ======================================================

st.markdown(
    '<div class="section-title">📈 Phân tích tăng trưởng</div>',
    unsafe_allow_html=True
)

growth_col1, growth_col2, growth_col3 = st.columns(3)


with growth_col1:

    if sales_growth >= 0:

        st.metric(
            "📈 Tăng trưởng doanh thu",
            f"{sales_growth:.2f}%",
            delta=f"{sales_growth:.2f}%"
        )

    else:

        st.metric(
            "📉 Tăng trưởng doanh thu",
            f"{sales_growth:.2f}%",
            delta=f"{sales_growth:.2f}%"
        )


with growth_col2:

    if profit_growth >= 0:

        st.metric(
            "📈 Tăng trưởng lợi nhuận",
            f"{profit_growth:.2f}%",
            delta=f"{profit_growth:.2f}%"
        )

    else:

        st.metric(
            "📉 Tăng trưởng lợi nhuận",
            f"{profit_growth:.2f}%",
            delta=f"{profit_growth:.2f}%"
        )


with growth_col3:

    st.metric(
        "💹 Biên lợi nhuận",
        f"{profit_margin:.2f}%"
    )


# ======================================================
# NHẬN ĐỊNH NHANH VỀ TĂNG TRƯỞNG
# ======================================================

if sales_growth > 0:

    st.success(
        f"""
        📈 **Doanh thu đang có xu hướng tăng**, đạt mức tăng trưởng
        **{sales_growth:.2f}%** so với kỳ tham chiếu.
        """
    )

elif sales_growth < 0:

    st.warning(
        f"""
        📉 **Doanh thu đang có xu hướng giảm**, mức tăng trưởng hiện tại
        là **{sales_growth:.2f}%** so với kỳ tham chiếu.
        Nhà quản lý cần xem xét nguyên nhân và các yếu tố ảnh hưởng đến doanh thu.
        """
    )

else:

    st.info(
        """
        ➡️ Doanh thu không có sự thay đổi đáng kể so với kỳ tham chiếu.
        """
    )


# ======================================================
# BIỂU ĐỒ DOANH THU THEO THỜI GIAN
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📈 Xu hướng doanh thu theo thời gian</div>',
    unsafe_allow_html=True
)

monthly_sales = get_monthly_sales(df)

st.plotly_chart(
    monthly_sales_chart(monthly_sales),
    use_container_width=True
)


# ======================================================
# DOANH THU THEO KHU VỰC & DANH MỤC
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🌍 Phân tích cơ cấu doanh thu</div>',
    unsafe_allow_html=True
)

sales_region = get_sales_by_region(df)

sales_category = get_sales_by_category(df)


left, right = st.columns(2)


with left:

    st.markdown("### 🌍 Doanh thu theo khu vực")

    st.plotly_chart(
        sales_by_region_chart(sales_region),
        use_container_width=True
    )


with right:

    st.markdown("### 🛍 Doanh thu theo danh mục")

    st.plotly_chart(
        sales_by_category_chart(sales_category),
        use_container_width=True
    )


# ======================================================
# PHÂN TÍCH KHU VỰC VÀ DANH MỤC TỐT NHẤT
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🏆 Kết quả nổi bật</div>',
    unsafe_allow_html=True
)

best_region = get_best_region(df)

best_category = get_best_category(df)


result_col1, result_col2 = st.columns(2)


with result_col1:

    st.success(
        f"""
        ### 🌍 Khu vực nổi bật

        **{best_region['Region']}**

        Lợi nhuận:

        **${best_region['Profit']:,.2f}**

        Đây là khu vực đang đóng góp hiệu quả nhất
        trong phạm vi dữ liệu được lựa chọn.
        """
    )


with result_col2:

    st.success(
        f"""
        ### 🛍 Danh mục nổi bật

        **{best_category['Category']}**

        Lợi nhuận:

        **${best_category['Profit']:,.2f}**

        Đây là danh mục đang mang lại hiệu quả
        nổi bật trong phạm vi phân tích.
        """
    )


# ======================================================
# INSIGHTS
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🤖 Thông tin kinh doanh</div>',
    unsafe_allow_html=True
)

insights = generate_insights(df)

if insights:

    for i, insight in enumerate(insights, start=1):

        st.info(
            f"**{i}.** {insight}"
        )

else:

    st.info(
        "Chưa có thông tin chuyên sâu cho phạm vi dữ liệu hiện tại."
    )


# ======================================================
# KHUYẾN NGHỊ
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🎯 Đề xuất chiến lược</div>',
    unsafe_allow_html=True
)

recommendations = generate_recommendations(df)

if recommendations:

    for i, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.warning(
            f"**{i}.** {recommendation}"
        )

else:

    st.info(
        "Chưa có đề xuất chiến lược cho phạm vi dữ liệu hiện tại."
    )


# ======================================================
# TÓM TẮT ĐIỀU HÀNH
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📋 Tóm tắt điều hành</div>',
    unsafe_allow_html=True
)

summary_col1, summary_col2 = st.columns(2)


with summary_col1:

    st.markdown(
        f"""
        <div class="info-box">

        <b>Quy mô kinh doanh</b><br><br>

        Tổng doanh thu đạt <b>${total_sales:,.2f}</b>,
        với <b>{total_orders:,}</b> đơn hàng và
        <b>{total_customers:,}</b> khách hàng.

        </div>
        """,
        unsafe_allow_html=True
    )


with summary_col2:

    if profit_margin >= 10:

        margin_status = "tương đối tốt"

    elif profit_margin >= 5:

        margin_status = "ở mức trung bình"

    else:

        margin_status = "cần được cải thiện"


    st.markdown(
        f"""
        <div class="info-box">

        <b>Hiệu quả sinh lợi</b><br><br>

        Biên lợi nhuận đạt <b>{profit_margin:.2f}%</b>,
        cho thấy hiệu quả sinh lợi hiện tại đang
        <b>{margin_status}</b>.

        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# KẾT LUẬN
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📝 Kết luận</div>',
    unsafe_allow_html=True
)

if sales_growth >= 0 and profit_growth >= 0:

    st.success(
        """
        Kết quả phân tích cho thấy hoạt động kinh doanh đang có
        xu hướng tích cực cả về doanh thu và lợi nhuận.
        Doanh nghiệp có thể tiếp tục tập trung nguồn lực vào
        các khu vực và danh mục đang có hiệu quả cao.
        """
    )

elif sales_growth < 0 and profit_growth < 0:

    st.warning(
        """
        Kết quả phân tích cho thấy cả doanh thu và lợi nhuận đều
        đang có xu hướng giảm. Doanh nghiệp cần ưu tiên rà soát
        các yếu tố ảnh hưởng đến doanh số, chi phí và hiệu quả
        kinh doanh để đưa ra giải pháp phù hợp.
        """
    )

else:

    st.info(
        """
        Kết quả phân tích cho thấy doanh thu và lợi nhuận có
        diễn biến khác nhau. Doanh nghiệp cần phân tích sâu hơn
        về cơ cấu sản phẩm, khu vực và khách hàng để xác định
        nguyên nhân và đưa ra quyết định phù hợp.
        """
    )


