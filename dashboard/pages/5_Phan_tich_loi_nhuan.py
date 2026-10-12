import os
import sys

# ============================================================
# 1. XÁC ĐỊNH THƯ MỤC GỐC CỦA PROJECT
# ============================================================

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, project_root)


# ============================================================
# 2. THƯ VIỆN
# ============================================================

import streamlit as st

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.analysis import (
    get_monthly_profit,
    get_profit_by_region,
    get_profit_by_category,
    get_top_profit_products
)

from src.visualization import (
    monthly_profit_chart,
    profit_by_region_chart,
    profit_by_category_chart,
    top_profit_products_chart,
    discount_profit_chart
)


# ============================================================
# 3. CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Phân tích Lợi nhuận",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 4. CSS GIAO DIỆN
# ============================================================

st.markdown(
    """
    <style>

    /* ===== Tiêu đề chính ===== */

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #17365D;
        margin-bottom: 5px;
    }

    .main-description {
        font-size: 16px;
        color: #666666;
        margin-bottom: 25px;
    }

    /* ===== Tiêu đề section ===== */

    .section-title {
        font-size: 22px;
        font-weight: 650;
        color: #17365D;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* ===== Đường phân cách ===== */

    hr {
        margin-top: 25px;
        margin-bottom: 25px;
    }

    /* ===== Sidebar ===== */

    section[data-testid="stSidebar"] {
        background-color: #F5F7FA;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="main-title">💰 Dashboard Phân tích Lợi nhuận</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-description">
        Phân tích hiệu quả sinh lợi của hoạt động kinh doanh dựa trên
        doanh thu, lợi nhuận, khu vực, danh mục sản phẩm và mức chiết khấu.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")


# ============================================================
# 6. TẢI DỮ LIỆU
# ============================================================

data_path = os.path.join(
    project_root,
    "data",
    "SampleSuperstore.csv"
)

df = load_data(data_path)

df = clean_data(df)


# ============================================================
# 7. BỘ LỌC
# ============================================================

st.sidebar.title("🔎 Bộ lọc Dashboard")

st.sidebar.caption(
    "Lựa chọn các tiêu chí để cập nhật toàn bộ phân tích."
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
    "📦 Danh mục",
    categories
)

selected_segment = st.sidebar.selectbox(
    "👥 Phân khúc khách hàng",
    segments
)


# ============================================================
# 8. ÁP DỤNG BỘ LỌC
# ============================================================

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


df = apply_filters(
    df,
    year=filter_year,
    region=filter_region,
    category=filter_category,
    segment=filter_segment
)


# ============================================================
# 9. KIỂM TRA DỮ LIỆU
# ============================================================

if df.empty:

    st.warning(
        "⚠️ Không có dữ liệu phù hợp với các điều kiện lọc hiện tại."
    )

    st.stop()


# ============================================================
# 10. TÍNH TOÁN KPI
# ============================================================

total_sales = df["Sales"].sum()

total_profit = df["Profit"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

average_profit = (
    df["Profit"].mean()
    if len(df) > 0
    else 0
)

average_discount = (
    df["Discount"].mean() * 100
    if "Discount" in df.columns
    else 0
)

average_sales = (
    df["Sales"].mean()
    if len(df) > 0
    else 0
)

negative_profit_count = (
    (df["Profit"] < 0).sum()
)


# ============================================================
# 11. KPI
# ============================================================

st.markdown(
    '<div class="section-title">📌 Chỉ số hiệu suất lợi nhuận</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="💰 Tổng lợi nhuận",
        value=f"${total_profit:,.2f}"
    )


with col2:

    st.metric(
        label="📈 Biên lợi nhuận",
        value=f"{profit_margin:.2f}%"
    )


with col3:

    st.metric(
        label="📊 Lợi nhuận trung bình",
        value=f"${average_profit:,.2f}"
    )


with col4:

    st.metric(
        label="💸 Chiết khấu trung bình",
        value=f"{average_discount:.2f}%"
    )


# ============================================================
# 12. KPI BỔ SUNG
# ============================================================

st.markdown("")

col5, col6, col7, col8 = st.columns(4)


with col5:

    st.metric(
        label="💵 Tổng doanh thu",
        value=f"${total_sales:,.2f}"
    )


with col6:

    st.metric(
        label="🧾 Số giao dịch",
        value=f"{len(df):,}"
    )


with col7:

    st.metric(
        label="💵 Doanh thu trung bình",
        value=f"${average_sales:,.2f}"
    )


with col8:

    st.metric(
        label="⚠️ Giao dịch lỗ",
        value=f"{negative_profit_count:,}"
    )


st.markdown("---")


# ============================================================
# 13. PHÂN TÍCH DỮ LIỆU
# ============================================================

monthly_profit = get_monthly_profit(df)

profit_region = get_profit_by_region(df)

profit_category = get_profit_by_category(df)

top_profit_products = get_top_profit_products(df)


# ============================================================
# 14. XU HƯỚNG LỢI NHUẬN THEO THỜI GIAN
# ============================================================

st.markdown(
    '<div class="section-title">📈 Xu hướng lợi nhuận theo thời gian</div>',
    unsafe_allow_html=True
)

st.caption(
    "Biểu đồ thể hiện sự biến động của lợi nhuận theo từng tháng, "
    "giúp nhận diện giai đoạn tăng trưởng hoặc suy giảm."
)

fig_monthly = monthly_profit_chart(
    monthly_profit
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ============================================================
# 15. LỢI NHUẬN THEO KHU VỰC
# ============================================================

st.markdown("---")

left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">🌍 Lợi nhuận theo khu vực</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "So sánh khả năng sinh lợi giữa các khu vực kinh doanh."
    )

    fig_region = profit_by_region_chart(
        profit_region
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ============================================================
# 16. LỢI NHUẬN THEO DANH MỤC
# ============================================================

with right:

    st.markdown(
        '<div class="section-title">📦 Lợi nhuận theo danh mục</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Đánh giá mức đóng góp lợi nhuận của từng nhóm sản phẩm."
    )

    fig_category = profit_by_category_chart(
        profit_category
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ============================================================
# 17. TOP SẢN PHẨM SINH LỜI
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🏆 Top 10 sản phẩm có lợi nhuận cao nhất</div>',
    unsafe_allow_html=True
)

st.caption(
    "Danh sách các sản phẩm đóng góp lợi nhuận cao nhất trong "
    "phạm vi dữ liệu đang được lựa chọn."
)

fig_top_products = top_profit_products_chart(
    top_profit_products
)

st.plotly_chart(
    fig_top_products,
    use_container_width=True
)


# ============================================================
# 18. CHIẾT KHẤU VÀ LỢI NHUẬN
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">💸 Mối quan hệ giữa chiết khấu và lợi nhuận</div>',
    unsafe_allow_html=True
)

st.caption(
    "Phân tích mối quan hệ giữa mức chiết khấu áp dụng và "
    "khả năng sinh lợi của đơn hàng."
)

fig_discount = discount_profit_chart(df)

st.plotly_chart(
    fig_discount,
    use_container_width=True
)


# ============================================================
# 19. NHẬN ĐỊNH TỰ ĐỘNG
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📝 Nhận định từ dữ liệu</div>',
    unsafe_allow_html=True
)


# ---- Khu vực tốt nhất ----

try:

    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    if not region_profit.empty:

        best_region = region_profit.idxmax()
        best_region_profit = region_profit.max()

        worst_region = region_profit.idxmin()
        worst_region_profit = region_profit.min()

        st.info(
            f"""
            🌍 **Phân bố lợi nhuận theo khu vực**

            Khu vực **{best_region}** đang có mức lợi nhuận cao nhất,
            đạt khoảng **${best_region_profit:,.2f}**.

            Trong khi đó, khu vực **{worst_region}** có mức lợi nhuận
            thấp nhất, khoảng **${worst_region_profit:,.2f}**.

            Điều này cho thấy hiệu quả kinh doanh có sự khác biệt
            giữa các khu vực và cần được xem xét riêng về doanh thu,
            chiết khấu và cơ cấu sản phẩm.
            """
        )

except Exception:

    st.info(
        "Chưa thể tạo nhận định về phân bố lợi nhuận theo khu vực."
    )


# ---- Danh mục tốt nhất ----

try:

    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    if not category_profit.empty:

        best_category = category_profit.idxmax()
        best_category_profit = category_profit.max()

        st.success(
            f"""
            📦 **Hiệu quả theo danh mục sản phẩm**

            Danh mục **{best_category}** đang tạo ra mức lợi nhuận
            cao nhất, đạt khoảng **${best_category_profit:,.2f}**.

            Đây là nhóm sản phẩm có đóng góp đáng kể vào hiệu quả
            sinh lợi của hoạt động kinh doanh.
            """
        )

except Exception:

    st.info(
        "Chưa thể tạo nhận định về hiệu quả theo danh mục."
    )


# ---- Chiết khấu ----

if average_discount > 0:

    st.warning(
        f"""
        💸 **Đánh giá chính sách chiết khấu**

        Mức chiết khấu trung bình hiện tại khoảng
        **{average_discount:.2f}%**.

        Do đó, doanh nghiệp cần theo dõi mối quan hệ giữa
        mức chiết khấu và lợi nhuận để hạn chế tình trạng
        tăng doanh số nhưng làm giảm hiệu quả sinh lợi.
        """
    )


# ============================================================
# 20. DỮ LIỆU CHI TIẾT
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📄 Dữ liệu sau khi lọc</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Hiển thị {len(df):,} dòng dữ liệu phù hợp với điều kiện lọc hiện tại."
)

st.dataframe(
    df,
    use_container_width=True,
    height=400
)