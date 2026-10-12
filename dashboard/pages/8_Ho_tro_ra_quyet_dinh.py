import os
import sys

# ======================================================
# XÁC ĐỊNH THƯ MỤC GỐC CỦA PROJECT
# ======================================================

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)


# ======================================================
# THƯ VIỆN
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ======================================================
# IMPORT MODULE DỰ ÁN
# ======================================================

from src.load_data import load_data
from src.cleaning import clean_data
from src.filter import apply_filters

from src.analysis import (
    recommend_region,
    recommend_category,
    recommend_product,
    recommend_customer,
    recommend_risk_region
)


# ======================================================
# CẤU HÌNH TRANG
# ======================================================

st.set_page_config(
    page_title="Hệ hỗ trợ ra quyết định",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================================================
# CSS GIAO DIỆN
# ======================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #123B66;
        margin-bottom: 5px;
    }

    .main-description {
        font-size: 16px;
        color: #5F6B7A;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #123B66;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# TIÊU ĐỀ
# ======================================================

st.markdown(
    '<div class="main-title">🤖 HỆ HỖ TRỢ RA QUYẾT ĐỊNH</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-description">
    Hệ thống phân tích dữ liệu bán hàng và đưa ra các khuyến nghị
    nhằm hỗ trợ nhà quản lý trong quá trình ra quyết định kinh doanh.
    </div>
    """,
    unsafe_allow_html=True
)


# ======================================================
# TẢI DỮ LIỆU
# ======================================================

try:

    df = load_data("data/SampleSuperstore.csv")
    df = clean_data(df)

except Exception as e:

    st.error(
        f"Không thể tải dữ liệu. Vui lòng kiểm tra lại đường dẫn dữ liệu.\n\n{e}"
    )

    st.stop()


# ======================================================
# SIDEBAR - BỘ LỌC
# ======================================================

st.sidebar.markdown("## 🔎 Bộ lọc dữ liệu")

st.sidebar.caption(
    "Các bộ lọc được áp dụng cho toàn bộ quá trình phân tích."
)


# ======================================================
# DANH SÁCH LỰA CHỌN
# ======================================================

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


# ======================================================
# BỘ LỌC GIAO DIỆN
# ======================================================

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


# ======================================================
# CHUYỂN GIÁ TRỊ GIAO DIỆN SANG LOGIC
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
        "⚠️ Không có dữ liệu phù hợp với bộ lọc hiện tại. "
        "Vui lòng thay đổi điều kiện lọc."
    )

    st.stop()


# ======================================================
# TỔNG QUAN DỮ LIỆU
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📊 Tổng quan dữ liệu phân tích</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Doanh thu",
        f"${df['Sales'].sum():,.2f}"
    )


with col2:

    st.metric(
        "📈 Lợi nhuận",
        f"${df['Profit'].sum():,.2f}"
    )


with col3:

    if "Order ID" in df.columns:
        orders = df["Order ID"].nunique()
    else:
        orders = len(df)

    st.metric(
        "🛒 Đơn hàng",
        f"{orders:,}"
    )


with col4:

    if "Customer ID" in df.columns:

        customers = df["Customer ID"].nunique()

    elif "Customer Name" in df.columns:

        customers = df["Customer Name"].nunique()

    else:

        customers = 0

    st.metric(
        "👥 Khách hàng",
        f"{customers:,}"
    )


# ======================================================
# LỰA CHỌN QUYẾT ĐỊNH
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🎯 Lựa chọn vấn đề cần hỗ trợ</div>',
    unsafe_allow_html=True
)

question = st.selectbox(
    "📌 Bạn muốn hệ thống hỗ trợ quyết định điều gì?",
    [
        "Nên đầu tư vào khu vực nào?",
        "Nên đẩy mạnh danh mục nào?",
        "Nên loại bỏ sản phẩm nào?",
        "Nên giữ chân khách hàng nào?",
        "Khu vực nào đang có rủi ro?"
    ]
)


st.caption(
    "Hãy lựa chọn một vấn đề và nhấn **Phân tích quyết định** "
    "để hệ thống đánh giá dữ liệu."
)


analyze = st.button(
    "🔍 Phân tích quyết định",
    type="primary",
    use_container_width=True
)


# ======================================================
# HÀM TẠO BIỂU ĐỒ
# ======================================================

def create_decision_chart(question, data):

    # ==================================================
    # KHU VỰC
    # ==================================================

    if question == "Nên đầu tư vào khu vực nào?":

        chart_df = (
            data.groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        fig = px.bar(
            chart_df,
            x="Region",
            y="Sales",
            text_auto=".2s",
            title="Doanh thu theo khu vực"
        )

        fig.update_layout(
            xaxis_title="Khu vực",
            yaxis_title="Doanh thu",
            template="plotly_white"
        )

        return fig


    # ==================================================
    # DANH MỤC
    # ==================================================

    elif question == "Nên đẩy mạnh danh mục nào?":

        chart_df = (
            data.groupby("Category")["Profit"]
            .sum()
            .reset_index()
            .sort_values("Profit", ascending=False)
        )

        fig = px.bar(
            chart_df,
            x="Category",
            y="Profit",
            text_auto=".2s",
            title="Lợi nhuận theo danh mục"
        )

        fig.update_layout(
            xaxis_title="Danh mục",
            yaxis_title="Lợi nhuận",
            template="plotly_white"
        )

        return fig


    # ==================================================
    # SẢN PHẨM
    # ==================================================

    elif question == "Nên loại bỏ sản phẩm nào?":

        chart_df = (
            data.groupby("Product Name")["Profit"]
            .sum()
            .sort_values()
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            chart_df,
            x="Profit",
            y="Product Name",
            orientation="h",
            text_auto=".2s",
            title="10 sản phẩm có lợi nhuận thấp nhất"
        )

        fig.update_layout(
            xaxis_title="Lợi nhuận",
            yaxis_title="Sản phẩm",
            template="plotly_white"
        )

        return fig


    # ==================================================
    # KHÁCH HÀNG
    # ==================================================

    elif question == "Nên giữ chân khách hàng nào?":

        chart_df = (
            data.groupby("Customer Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            chart_df,
            x="Sales",
            y="Customer Name",
            orientation="h",
            text_auto=".2s",
            title="10 khách hàng có doanh thu cao nhất"
        )

        fig.update_layout(
            xaxis_title="Doanh thu",
            yaxis_title="Khách hàng",
            template="plotly_white"
        )

        return fig


    # ==================================================
    # RỦI RO KHU VỰC
    # ==================================================

    else:

        chart_df = (
            data.groupby("Region")["Profit"]
            .sum()
            .reset_index()
            .sort_values("Profit")
        )

        fig = px.bar(
            chart_df,
            x="Region",
            y="Profit",
            text_auto=".2s",
            title="Lợi nhuận theo khu vực"
        )

        fig.update_layout(
            xaxis_title="Khu vực",
            yaxis_title="Lợi nhuận",
            template="plotly_white"
        )

        return fig


# ======================================================
# PHÂN TÍCH QUYẾT ĐỊNH
# ======================================================

if analyze:

    with st.spinner("🔄 Hệ thống đang phân tích dữ liệu..."):

        # ==================================================
        # KHU VỰC
        # ==================================================

        if question == "Nên đầu tư vào khu vực nào?":

            result = recommend_region(df)

            priority = "🔴 Cao"

            chart_df = (
                df.groupby("Region")["Sales"]
                .sum()
                .reset_index()
            )

            total_value = chart_df["Sales"].sum()

            selected_value = chart_df.loc[
                chart_df["Region"] == result["ket_qua"],
                "Sales"
            ]

            if not selected_value.empty:
                selected_value = selected_value.iloc[0]
            else:
                selected_value = 0

            metric_name = "Doanh thu"

            value = selected_value

            if total_value != 0:
                percentage = (
                    selected_value /
                    total_value
                ) * 100
            else:
                percentage = 0


        # ==================================================
        # DANH MỤC
        # ==================================================

        elif question == "Nên đẩy mạnh danh mục nào?":

            result = recommend_category(df)

            priority = "🟠 Trung bình"

            chart_df = (
                df.groupby("Category")["Profit"]
                .sum()
                .reset_index()
            )

            total_value = chart_df["Profit"].sum()

            selected_value = chart_df.loc[
                chart_df["Category"] == result["ket_qua"],
                "Profit"
            ]

            if not selected_value.empty:
                selected_value = selected_value.iloc[0]
            else:
                selected_value = 0

            metric_name = "Lợi nhuận"

            value = selected_value

            if total_value != 0:
                percentage = (
                    selected_value /
                    total_value
                ) * 100
            else:
                percentage = 0


        # ==================================================
        # SẢN PHẨM
        # ==================================================

        elif question == "Nên loại bỏ sản phẩm nào?":

            result = recommend_product(df)

            priority = "🔴 Cao"

            product_profit = (
                df.groupby("Product Name")["Profit"]
                .sum()
                .sort_values()
            )

            selected_value = product_profit.get(
                result["ket_qua"],
                0
            )

            total_sales = df["Sales"].sum()

            metric_name = "Lợi nhuận"

            value = selected_value

            if total_sales != 0:
                percentage = (
                    abs(selected_value) /
                    total_sales
                ) * 100
            else:
                percentage = 0


        # ==================================================
        # KHÁCH HÀNG
        # ==================================================

        elif question == "Nên giữ chân khách hàng nào?":

            result = recommend_customer(df)

            priority = "🟢 Quan trọng"

            customer_sales = (
                df.groupby("Customer Name")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            selected_value = customer_sales.get(
                result["ket_qua"],
                0
            )

            total_value = df["Sales"].sum()

            metric_name = "Doanh thu"

            value = selected_value

            if total_value != 0:
                percentage = (
                    selected_value /
                    total_value
                ) * 100
            else:
                percentage = 0


        # ==================================================
        # RỦI RO
        # ==================================================

        else:

            result = recommend_risk_region(df)

            priority = "🔴 Khẩn cấp"

            chart_df = (
                df.groupby("Region")["Profit"]
                .sum()
                .reset_index()
            )

            selected_value = chart_df.loc[
                chart_df["Region"] == result["ket_qua"],
                "Profit"
            ]

            if not selected_value.empty:
                selected_value = selected_value.iloc[0]
            else:
                selected_value = 0

            total_value = df["Profit"].sum()

            metric_name = "Lợi nhuận"

            value = selected_value

            if total_value != 0:
                percentage = (
                    selected_value /
                    total_value
                ) * 100
            else:
                percentage = 0


        # ==================================================
        # BIỂU ĐỒ
        # ==================================================

        fig = create_decision_chart(
            question,
            df
        )


    # ==================================================
    # KẾT QUẢ QUYẾT ĐỊNH
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🎯 Kết quả quyết định</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"👉 Hệ thống đề xuất: **{result['ket_qua']}**"
    )


    # ==================================================
    # KPI KẾT QUẢ
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            f"📊 {metric_name}",
            f"${value:,.2f}"
        )


    with col2:

        st.metric(
            "📌 Tỷ trọng",
            f"{percentage:.2f}%"
        )


    with col3:

        st.metric(
            "⚡ Mức ưu tiên",
            priority
        )


    with col4:

        if percentage >= 40:
            confidence = "Rất cao"

        elif percentage >= 20:
            confidence = "Cao"

        elif percentage >= 10:
            confidence = "Trung bình"

        else:
            confidence = "Thấp"

        st.metric(
            "🔬 Độ tin cậy",
            confidence
        )


    # ==================================================
    # CƠ SỞ QUYẾT ĐỊNH
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🔬 Cơ sở của quyết định</div>',
        unsafe_allow_html=True
    )

    st.info(
        f"""
        **Loại quyết định:** {question}

        **Đối tượng được đề xuất:** {result['ket_qua']}

        **Chỉ tiêu chính:** {metric_name}

        **Giá trị:** ${value:,.2f}

        **Tỷ trọng trong phạm vi dữ liệu:** {percentage:.2f}%

        **Mức ưu tiên:** {priority}
        """
    )


    # ==================================================
    # LÝ DO
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📋 Các yếu tố dẫn đến quyết định</div>',
        unsafe_allow_html=True
    )

    reasons = result.get(
        "ly_do",
        []
    )

    if reasons:

        for i, reason in enumerate(
            reasons,
            start=1
        ):

            st.write(
                f"**{i}.** {reason}"
            )

    else:

        st.write(
            "Hệ thống chưa cung cấp danh sách lý do chi tiết."
        )


    # ==================================================
    # KHUYẾN NGHỊ
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">💡 Khuyến nghị hành động</div>',
        unsafe_allow_html=True
    )

    st.warning(
        result.get(
            "khuyen_nghi",
            "Chưa có khuyến nghị."
        )
    )


    # ==================================================
    # BIỂU ĐỒ
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📈 Dữ liệu hỗ trợ quyết định</div>',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ==================================================
    # BẢNG XẾP HẠNG
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Bảng dữ liệu phân tích</div>',
        unsafe_allow_html=True
    )


    # ==================================================
    # TẠO BẢNG THEO TỪNG LOẠI QUYẾT ĐỊNH
    # ==================================================

    if question == "Nên đầu tư vào khu vực nào?":

        ranking = (
            df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values(
                "Sales",
                ascending=False
            )
        )

        ranking["Tỷ trọng (%)"] = (
            ranking["Sales"] /
            ranking["Sales"].sum()
        ) * 100

        ranking = ranking.head(10)


    elif question == "Nên đẩy mạnh danh mục nào?":

        ranking = (
            df.groupby("Category")["Profit"]
            .sum()
            .reset_index()
            .sort_values(
                "Profit",
                ascending=False
            )
        )

        ranking["Tỷ trọng (%)"] = (
            ranking["Profit"] /
            ranking["Profit"].sum()
        ) * 100

        ranking = ranking.head(10)


    elif question == "Nên loại bỏ sản phẩm nào?":

        ranking = (
            df.groupby("Product Name")["Profit"]
            .sum()
            .reset_index()
            .sort_values(
                "Profit",
                ascending=True
            )
            .head(10)
        )


    elif question == "Nên giữ chân khách hàng nào?":

        ranking = (
            df.groupby("Customer Name")["Sales"]
            .sum()
            .reset_index()
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(10)
        )

        ranking["Tỷ trọng (%)"] = (
            ranking["Sales"] /
            ranking["Sales"].sum()
        ) * 100


    else:

        ranking = (
            df.groupby("Region")["Profit"]
            .sum()
            .reset_index()
            .sort_values(
                "Profit",
                ascending=True
            )
        )


    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )


    # ==================================================
    # BÁO CÁO QUYẾT ĐỊNH
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📄 Báo cáo quyết định</div>',
        unsafe_allow_html=True
    )

    report = pd.DataFrame(
        {
            "Câu hỏi": [question],

            "Đối tượng đề xuất": [
                result["ket_qua"]
            ],

            "Chỉ tiêu": [
                metric_name
            ],

            "Giá trị": [
                round(value, 2)
            ],

            "Tỷ trọng (%)": [
                round(percentage, 2)
            ],

            "Mức ưu tiên": [
                priority
            ],

            "Độ tin cậy": [
                confidence
            ],

            "Khuyến nghị": [
                result.get(
                    "khuyen_nghi",
                    ""
                )
            ]
        }
    )


    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )


    # ==================================================
    # DOWNLOAD CSV
    # ==================================================

    csv = report.to_csv(
        index=False
    ).encode("utf-8-sig")


    st.download_button(
        label="⬇️ Tải báo cáo quyết định (.CSV)",
        data=csv,
        file_name="Decision_Report.csv",
        mime="text/csv",
        use_container_width=True
    )


    # ==================================================
    # KẾT LUẬN
    # ==================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📝 Kết luận</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"""
        Dựa trên dữ liệu sau khi áp dụng các bộ lọc,
        hệ thống xác định **{result['ket_qua']}** là đối tượng
        cần được ưu tiên đối với quyết định:

        **"{question}"**

        Đối tượng này có giá trị **${value:,.2f}**,
        tương ứng khoảng **{percentage:.2f}%**
        trong phạm vi dữ liệu đang phân tích.

        **Khuyến nghị:** {result.get('khuyen_nghi', '')}
        """
    )


# ======================================================
# TRẠNG THÁI CHƯA PHÂN TÍCH
# ======================================================

else:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">ℹ️ Hướng dẫn sử dụng</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.info(
            """
            **Bước 1**

            Sử dụng bộ lọc bên trái để
            lựa chọn phạm vi dữ liệu cần phân tích.
            """
        )


    with col2:

        st.info(
            """
            **Bước 2**

            Chọn vấn đề kinh doanh mà
            bạn muốn hệ thống hỗ trợ.
            """
        )


    with col3:

        st.info(
            """
            **Bước 3**

            Nhấn **Phân tích quyết định**
            để nhận kết quả và khuyến nghị.
            """
        )


    st.markdown("---")

    st.caption(
        "💡 Hệ thống sử dụng dữ liệu bán hàng hiện tại "
        "để hỗ trợ phân tích và ra quyết định. "
        "Kết quả nên được kết hợp với các yếu tố thực tế "
        "trước khi đưa ra quyết định kinh doanh cuối cùng."
    )

