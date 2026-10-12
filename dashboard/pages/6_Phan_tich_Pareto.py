import os
import sys

# =========================================================
# THIẾT LẬP ĐƯỜNG DẪN PROJECT
# =========================================================

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)


# =========================================================
# THƯ VIỆN
# =========================================================

import streamlit as st


# =========================================================
# IMPORT MODULE DỰ ÁN
# =========================================================

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.analysis import (
    get_product_pareto,
    get_customer_pareto
)

from src.visualization import (
    pareto_product_chart,
    pareto_customer_chart
)


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Phân tích Pareto",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CSS GIAO DIỆN
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #123B66;
        margin-bottom: 5px;
    }

    .description {
        font-size: 16px;
        color: #5F6B7A;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #123B66;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .analysis-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E1E7EF;
        background-color: #FFFFFF;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    """
    <div class="main-title">
        📊 PHÂN TÍCH PARETO – QUY TẮC 80/20
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="description">
        Phân tích Pareto giúp xác định nhóm sản phẩm và khách hàng
        có mức đóng góp lớn vào tổng doanh thu. Kết quả hỗ trợ nhà quản lý
        xác định đối tượng trọng điểm và ưu tiên nguồn lực kinh doanh.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")


# =========================================================
# TẢI DỮ LIỆU
# =========================================================

try:

    df = load_data(
        "data/SampleSuperstore.csv"
    )

    df = clean_data(df)

except Exception as e:

    st.error(
        f"""
        Không thể tải dữ liệu.

        Vui lòng kiểm tra:
        - Đường dẫn file dữ liệu.
        - File SampleSuperstore.csv.
        - Các module trong thư mục src.

        Chi tiết lỗi: {e}
        """
    )

    st.stop()


# =========================================================
# SIDEBAR – BỘ LỌC
# =========================================================

st.sidebar.markdown(
    "## 🔎 Bộ lọc Dashboard"
)

st.sidebar.caption(
    "Lựa chọn phạm vi dữ liệu dùng cho phân tích Pareto."
)


# =========================================================
# DANH SÁCH BỘ LỌC
# =========================================================

years = (
    ["Tất cả"]
    + sorted(
        df["Year"]
        .dropna()
        .unique()
        .tolist()
    )
)

regions = (
    ["Tất cả"]
    + sorted(
        df["Region"]
        .dropna()
        .unique()
        .tolist()
    )
)

categories = (
    ["Tất cả"]
    + sorted(
        df["Category"]
        .dropna()
        .unique()
        .tolist()
    )
)

segments = (
    ["Tất cả"]
    + sorted(
        df["Segment"]
        .dropna()
        .unique()
        .tolist()
    )
)


# =========================================================
# BỘ LỌC GIAO DIỆN
# =========================================================

selected_year = st.sidebar.selectbox(
    "📅 Năm",
    years,
    index=0
)

selected_region = st.sidebar.selectbox(
    "🌍 Khu vực",
    regions,
    index=0
)

selected_category = st.sidebar.selectbox(
    "📦 Danh mục",
    categories,
    index=0
)

selected_segment = st.sidebar.selectbox(
    "👥 Phân khúc khách hàng",
    segments,
    index=0
)


# =========================================================
# CHUYỂN ĐỔI GIÁ TRỊ BỘ LỌC
# =========================================================

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


# =========================================================
# ÁP DỤNG BỘ LỌC
# =========================================================

df_filtered = apply_filters(
    df,
    year=filter_year,
    region=filter_region,
    category=filter_category,
    segment=filter_segment
)


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if df_filtered.empty:

    st.warning(
        """
        ⚠️ Không có dữ liệu phù hợp với các điều kiện
        lọc hiện tại.

        Vui lòng thay đổi bộ lọc và thử lại.
        """
    )

    st.stop()


# =========================================================
# PHÂN TÍCH PARETO
# =========================================================

try:

    product_pareto = get_product_pareto(
        df_filtered
    )

    customer_pareto = get_customer_pareto(
        df_filtered
    )

except Exception as e:

    st.error(
        f"""
        Không thể thực hiện phân tích Pareto.

        Vui lòng kiểm tra các hàm:
        - get_product_pareto()
        - get_customer_pareto()

        Chi tiết lỗi: {e}
        """
    )

    st.stop()


# =========================================================
# KIỂM TRA KẾT QUẢ
# =========================================================

if product_pareto.empty:

    st.warning(
        "Không có dữ liệu sản phẩm để thực hiện phân tích Pareto."
    )


if customer_pareto.empty:

    st.warning(
        "Không có dữ liệu khách hàng để thực hiện phân tích Pareto."
    )


# =========================================================
# PARETO SẢN PHẨM
# =========================================================

if not product_pareto.empty:

    st.markdown(
        """
        <div class="section-title">
            📦 Pareto doanh thu theo sản phẩm
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Biểu đồ sắp xếp sản phẩm theo doanh thu từ cao xuống thấp,
        đồng thời thể hiện doanh thu tích lũy. Phân tích giúp xác định
        nhóm sản phẩm đang đóng góp lớn nhất vào kết quả kinh doanh.
        """
    )

    # Chỉ lấy Top 20 để biểu đồ dễ quan sát
    product_chart = product_pareto.head(20)

    st.plotly_chart(
        pareto_product_chart(
            product_chart
        ),
        use_container_width=True
    )

    # -----------------------------------------------------
    # NHẬN ĐỊNH
    # -----------------------------------------------------

    top_product = product_pareto.iloc[0]

    st.info(
        f"""
        **📌 Nhận định sản phẩm**

        Sản phẩm có doanh thu cao nhất trong phạm vi dữ liệu
        hiện tại là:

        **{top_product['Product Name']}**

        với doanh thu:

        **${top_product['Sales']:,.2f}**

        Đây là sản phẩm cần được theo dõi về doanh số,
        tồn kho và khả năng duy trì nhu cầu thị trường.
        """
    )


st.markdown("---")


# =========================================================
# PARETO KHÁCH HÀNG
# =========================================================

if not customer_pareto.empty:

    st.markdown(
        """
        <div class="section-title">
            👥 Pareto doanh thu theo khách hàng
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Phân tích Pareto khách hàng giúp xác định những khách hàng
        có giá trị doanh thu cao, từ đó hỗ trợ doanh nghiệp xây dựng
        chính sách chăm sóc và duy trì khách hàng trọng điểm.
        """
    )

    # Chỉ lấy Top 20 để biểu đồ dễ quan sát
    customer_chart = customer_pareto.head(20)

    st.plotly_chart(
        pareto_customer_chart(
            customer_chart
        ),
        use_container_width=True
    )

    # -----------------------------------------------------
    # NHẬN ĐỊNH
    # -----------------------------------------------------

    top_customer = customer_pareto.iloc[0]

    st.info(
        f"""
        **📌 Nhận định khách hàng**

        Khách hàng có doanh thu cao nhất trong phạm vi dữ liệu
        hiện tại là:

        **{top_customer['Customer Name']}**

        với doanh thu:

        **${top_customer['Sales']:,.2f}**

        Nhóm khách hàng có doanh thu cao cần được ưu tiên
        trong các chương trình chăm sóc và duy trì quan hệ.
        """
    )


st.markdown("---")


# =========================================================
# ĐỀ XUẤT QUẢN TRỊ
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🎯 Đề xuất quản trị
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# =========================================================
# ĐỀ XUẤT SẢN PHẨM
# =========================================================

with col1:

    st.success(
        """
        **📦 Đối với sản phẩm**

        • Ưu tiên đảm bảo tồn kho đối với các sản phẩm
        có doanh thu cao.

        • Theo dõi thường xuyên biến động doanh thu
        của nhóm sản phẩm chủ lực.

        • Tập trung hoạt động marketing vào các sản phẩm
        có khả năng tạo doanh thu lớn.

        • Đánh giá định kỳ các sản phẩm có doanh thu thấp
        để tối ưu danh mục.
        """
    )


# =========================================================
# ĐỀ XUẤT KHÁCH HÀNG
# =========================================================

with col2:

    st.info(
        """
        **👥 Đối với khách hàng**

        • Xây dựng chính sách chăm sóc riêng cho khách hàng
        có giá trị cao.

        • Triển khai chương trình khách hàng thân thiết.

        • Theo dõi sự thay đổi doanh thu của nhóm khách hàng
        trọng điểm.

        • Chủ động duy trì quan hệ với những khách hàng
        có đóng góp lớn.
        """
    )


st.markdown("---")


# =========================================================
# BẢNG CHI TIẾT SẢN PHẨM
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📄 Chi tiết Pareto sản phẩm
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander(
    "📦 Mở bảng dữ liệu Pareto sản phẩm"
):

    st.dataframe(
        product_pareto,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# BẢNG CHI TIẾT KHÁCH HÀNG
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📄 Chi tiết Pareto khách hàng
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander(
    "👥 Mở bảng dữ liệu Pareto khách hàng"
):

    st.dataframe(
        customer_pareto,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# KẾT LUẬN
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="section-title">
        📝 Kết luận
    </div>
    """,
    unsafe_allow_html=True
)

st.success(
    """
    Phân tích Pareto cung cấp góc nhìn về mức độ tập trung
    doanh thu giữa các sản phẩm và khách hàng.

    Kết quả có thể được sử dụng làm cơ sở để doanh nghiệp
    ưu tiên nguồn lực cho nhóm sản phẩm chủ lực và khách hàng
    có giá trị cao, đồng thời theo dõi những đối tượng có
    đóng góp thấp để tối ưu hiệu quả kinh doanh.
    """
)