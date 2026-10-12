import os
import sys

# =========================================================
# THIẾT LẬP ĐƯỜNG DẪN PROJECT
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# THƯ VIỆN
# =========================================================

import streamlit as st

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.analysis import (
    get_sales_map,
    get_profit_map
)

from src.visualization import (
    sales_map_chart,
    profit_map_chart
)


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Phân tích Bản đồ",
    page_icon="🗺️",
    layout="wide"
)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🗺️ Phân tích Doanh số và Lợi nhuận theo Địa lý")

st.caption(
    "Phân tích sự phân bố hiệu quả kinh doanh theo khu vực, "
    "hỗ trợ xác định thị trường có hiệu suất cao và các khu vực cần cải thiện."
)

st.markdown("---")


# =========================================================
# TẢI DỮ LIỆU
# =========================================================

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "SampleSuperstore.csv"
)

df = load_data(DATA_PATH)
df = clean_data(df)


# =========================================================
# BỘ LỌC DASHBOARD
# =========================================================

st.sidebar.title("🔎 Bộ lọc Dashboard")

st.sidebar.caption(
    "Lựa chọn các điều kiện để thay đổi phạm vi phân tích."
)

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


# =========================================================
# ÁP DỤNG BỘ LỌC
# =========================================================

df = apply_filters(
    df,
    year=(
        "All"
        if selected_year == "Tất cả"
        else selected_year
    ),
    region=(
        "All"
        if selected_region == "Tất cả"
        else selected_region
    ),
    category=(
        "All"
        if selected_category == "Tất cả"
        else selected_category
    ),
    segment=(
        "All"
        if selected_segment == "Tất cả"
        else selected_segment
    )
)


# =========================================================
# PHÂN TÍCH DỮ LIỆU BẢN ĐỒ
# =========================================================

sales_map = get_sales_map(df)
profit_map = get_profit_map(df)


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if sales_map.empty or profit_map.empty:

    st.warning(
        "⚠️ Không có dữ liệu phù hợp với các điều kiện lọc hiện tại."
    )

    st.stop()


# =========================================================
# XÁC ĐỊNH KHU VỰC
# =========================================================

best_sales = sales_map.loc[
    sales_map["Sales"].idxmax()
]

best_profit = profit_map.loc[
    profit_map["Profit"].idxmax()
]

worst_profit = profit_map.loc[
    profit_map["Profit"].idxmin()
]


# =========================================================
# 1. CHỈ SỐ HIỆU SUẤT ĐỊA LÝ
# =========================================================

st.subheader("📌 Chỉ số hiệu suất theo Địa lý")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Tổng doanh số",
        f"${sales_map['Sales'].sum():,.2f}"
    )


with col2:

    st.metric(
        "📈 Tổng lợi nhuận",
        f"${profit_map['Profit'].sum():,.2f}"
    )


with col3:

    st.metric(
        "🏆 Doanh số cao nhất",
        best_sales["State/Province"],
        f"${best_sales['Sales']:,.2f}"
    )


with col4:

    st.metric(
        "💎 Lợi nhuận cao nhất",
        best_profit["State/Province"],
        f"${best_profit['Profit']:,.2f}"
    )


st.markdown("---")


# =========================================================
# 2. PHÂN BỐ TRÊN BẢN ĐỒ
# =========================================================

st.subheader("🗺️ Phân bố hiệu quả kinh doanh theo địa lý")

st.caption(
    "Bản đồ thể hiện sự phân bố doanh số và lợi nhuận "
    "giữa các bang/khu vực trong tập dữ liệu."
)


left, right = st.columns(2)


# ---------------------------------------------------------
# BẢN ĐỒ DOANH SỐ
# ---------------------------------------------------------

with left:

    st.markdown("### 💰 Phân bổ Doanh số")

    st.plotly_chart(
        sales_map_chart(sales_map),
        use_container_width=True
    )


# ---------------------------------------------------------
# BẢN ĐỒ LỢI NHUẬN
# ---------------------------------------------------------

with right:

    st.markdown("### 📈 Phân bổ Lợi nhuận")

    st.plotly_chart(
        profit_map_chart(profit_map),
        use_container_width=True
    )


st.markdown("---")


# =========================================================
# 3. XẾP HẠNG KHU VỰC
# =========================================================

st.subheader("🏆 Xếp hạng hiệu quả theo khu vực")

left, right = st.columns(2)


# ---------------------------------------------------------
# DOANH SỐ
# ---------------------------------------------------------

with left:

    st.markdown("### 💰 Top khu vực theo Doanh số")

    sales_table = sales_map.sort_values(
        "Sales",
        ascending=False
    ).copy()

    st.dataframe(
        sales_table,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# LỢI NHUẬN
# ---------------------------------------------------------

with right:

    st.markdown("### 📈 Top khu vực theo Lợi nhuận")

    profit_table = profit_map.sort_values(
        "Profit",
        ascending=False
    ).copy()

    st.dataframe(
        profit_table,
        use_container_width=True,
        hide_index=True
    )


st.markdown("---")


# =========================================================
# 4. NHẬN ĐỊNH TỪ DỮ LIỆU
# =========================================================

st.subheader("📋 Nhận định từ dữ liệu")


# ---------------------------------------------------------
# NHẬN ĐỊNH 1
# ---------------------------------------------------------

st.info(
    f"""
    **🌍 Phân bố doanh số**

    Khu vực **{best_sales["State/Province"]}** đang có
    mức doanh số cao nhất trong phạm vi dữ liệu được lựa chọn,
    đạt **${best_sales["Sales"]:,.2f}**.

    Kết quả cho thấy đây là một trong những khu vực có
    đóng góp đáng kể vào hoạt động kinh doanh.
    """
)


# ---------------------------------------------------------
# NHẬN ĐỊNH 2
# ---------------------------------------------------------

st.success(
    f"""
    **📈 Hiệu quả sinh lợi**

    Khu vực **{best_profit["State/Province"]}** đang tạo ra
    mức lợi nhuận cao nhất, đạt **${best_profit["Profit"]:,.2f}**.

    Đây là khu vực cần được duy trì và tiếp tục khai thác
    nhằm đảm bảo hiệu quả sinh lời.
    """
)


# ---------------------------------------------------------
# NHẬN ĐỊNH 3
# ---------------------------------------------------------

st.warning(
    f"""
    **⚠️ Khu vực cần cải thiện**

    Khu vực **{worst_profit["State/Province"]}** có mức
    lợi nhuận thấp nhất, đạt **${worst_profit["Profit"]:,.2f}**.

    Doanh nghiệp nên xem xét chính sách giá, mức chiết khấu,
    cơ cấu sản phẩm và chi phí vận hành tại khu vực này.
    """
)


st.markdown("---")


# =========================================================
# 5. HỖ TRỢ RA QUYẾT ĐỊNH
# =========================================================

st.subheader("🤖 Hỗ trợ ra quyết định")

left, right = st.columns(2)


with left:

    st.success(
        f"""
        **🎯 Ưu tiên khu vực có doanh số cao**

        Tiếp tục duy trì hoạt động kinh doanh tại
        **{best_sales["State/Province"]}**.

        Có thể xem xét mở rộng danh mục sản phẩm,
        tăng cường hoạt động marketing và chăm sóc khách hàng
        tại khu vực này.

        **Doanh số hiện tại:**
        ${best_sales["Sales"]:,.2f}
        """
    )


with right:

    st.warning(
        f"""
        **⚠️ Kiểm soát khu vực có lợi nhuận thấp**

        Cần đánh giá lại chính sách giá, chiết khấu,
        danh mục sản phẩm và chi phí vận hành tại
        **{worst_profit["State/Province"]}**.

        Mục tiêu là cải thiện khả năng sinh lợi
        và hạn chế các hoạt động kinh doanh kém hiệu quả.

        **Lợi nhuận hiện tại:**
        ${worst_profit["Profit"]:,.2f}
        """
    )


st.markdown("---")


# =========================================================
# 6. DỮ LIỆU CHI TIẾT
# =========================================================

st.subheader("📄 Dữ liệu phân tích chi tiết")

with st.expander("🔽 Xem bảng doanh số theo khu vực"):

    st.dataframe(
        sales_map,
        use_container_width=True,
        hide_index=True
    )


with st.expander("🔽 Xem bảng lợi nhuận theo khu vực"):

    st.dataframe(
        profit_map,
        use_container_width=True,
        hide_index=True
    )