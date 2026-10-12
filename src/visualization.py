import plotly.express as px
import plotly.graph_objects as go


# ==========================
# DOANH SỐ HÀNG THÁNG
# ==========================
def monthly_sales_chart(df):

    fig = px.line(
        df,
        x="YearMonth",
        y="Sales",
        title="Xu hướng Doanh số hàng tháng",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Tháng",
        yaxis_title="Doanh số"
    )

    return fig


# ==========================
# DOANH SỐ THEO KHU VỰC
# ==========================
def sales_by_region_chart(df):

    fig = px.bar(
        df,
        x="Region",
        y="Sales",
        title="Doanh số theo Khu vực",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Khu vực",
        yaxis_title="Doanh số"
    )

    return fig


# ==========================
# DOANH SỐ THEO DANH MỤC
# ==========================
def sales_by_category_chart(df):

    fig = px.pie(
        df,
        names="Category",
        values="Sales",
        title="Tỷ trọng Doanh số theo Danh mục",
        hole=0.4
    )

    return fig


# ==========================
# TOP SẢN PHẨM
# ==========================
def top_products_chart(df):

    fig = px.bar(
        df,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Sản phẩm doanh thu cao nhất",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Doanh số",
        yaxis_title="Tên sản phẩm",
        yaxis=dict(categoryorder="total ascending")
    )

    return fig


# ==========================
# TOP KHÁCH HÀNG
# ==========================
def top_customers_chart(df):

    fig = px.bar(
        df,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Top 10 Khách hàng tiêu biểu",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Doanh số",
        yaxis_title="Tên khách hàng",
        yaxis=dict(categoryorder="total ascending")
    )

    return fig


# ==========================
# DOANH SỐ THEO BANG
# ==========================
def sales_by_state_chart(df):

    state_column = "State/Province"

    if "State" in df.columns:
        state_column = "State"

    fig = px.bar(
        df.head(10),
        x="Sales",
        y=state_column,
        orientation="h",
        title="Top 10 Bang có doanh số cao nhất",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Doanh số",
        yaxis_title="Bang/Tỉnh thành",
        yaxis=dict(categoryorder="total ascending")
    )

    return fig


# ==========================
# TOP DANH MỤC PHỤ
# ==========================
def top_subcategory_chart(df):

    fig = px.bar(
        df,
        x="Sub-Category",
        y="Sales",
        title="Doanh số theo Danh mục phụ",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Danh mục phụ",
        yaxis_title="Doanh số"
    )

    return fig


# ======================================================
#               BIỂU ĐỒ LỢI NHUẬN
# ======================================================

# ==========================
# LỢI NHUẬN HÀNG THÁNG
# ==========================
def monthly_profit_chart(df):

    fig = px.line(
        df,
        x="YearMonth",
        y="Profit",
        title="Xu hướng Lợi nhuận hàng tháng",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Tháng",
        yaxis_title="Lợi nhuận"
    )

    return fig


# ==========================
# LỢI NHUẬN THEO KHU VỰC
# ==========================
def profit_by_region_chart(df):

    fig = px.bar(
        df,
        x="Region",
        y="Profit",
        title="Lợi nhuận theo Khu vực",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Khu vực",
        yaxis_title="Lợi nhuận"
    )

    return fig


# ==========================
# LỢI NHUẬN THEO DANH MỤC
# ==========================
def profit_by_category_chart(df):

    fig = px.pie(
        df,
        names="Category",
        values="Profit",
        title="Tỷ trọng Lợi nhuận theo Danh mục",
        hole=0.4
    )

    return fig


# ==========================
# TOP SẢN PHẨM THEO LỢI NHUẬN
# ==========================
def top_profit_products_chart(df):

    fig = px.bar(
        df,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Sản phẩm có lợi nhuận cao nhất",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Lợi nhuận",
        yaxis_title="Tên sản phẩm",
        yaxis=dict(categoryorder="total ascending")
    )

    return fig


# ==========================
# CHIẾT KHẤU VS LỢI NHUẬN
# ==========================
def discount_profit_chart(df):

    fig = px.scatter(
        df,
        x="Discount",
        y="Profit",
        color="Category",
        size="Sales",
        hover_name="Product Name",
        title="Mối quan hệ giữa Chiết khấu và Lợi nhuận"
    )

    fig.update_layout(
        xaxis_title="Chiết khấu",
        yaxis_title="Lợi nhuận"
    )

    return fig


# ==========================
# BIỂU ĐỒ SỐ LƯỢNG
# ==========================

def quantity_by_category_chart(df):

    fig = px.bar(
        df,
        x="Category",
        y="Quantity",
        title="Số lượng bán ra theo Danh mục",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Danh mục",
        yaxis_title="Số lượng"
    )

    return fig


def quantity_by_region_chart(df):

    fig = px.bar(
        df,
        x="Region",
        y="Quantity",
        title="Số lượng bán ra theo Khu vực",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Khu vực",
        yaxis_title="Số lượng"
    )

    return fig


def quantity_by_subcategory_chart(df):

    fig = px.bar(
        df,
        x="Sub-Category",
        y="Quantity",
        title="Số lượng bán ra theo Danh mục phụ",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Danh mục phụ",
        yaxis_title="Số lượng"
    )

    return fig


# ==========================
# PHÂN KHÚC KHÁCH HÀNG
# ==========================

def sales_by_segment_chart(df):

    fig = px.pie(
        df,
        names="Segment",
        values="Sales",
        title="Doanh số theo Phân khúc khách hàng"
    )

    return fig


def customer_segment_chart(df):

    fig = px.bar(
        df,
        x="Segment",
        y="Customers",
        text_auto=True,
        title="Số lượng khách hàng theo Phân khúc"
    )

    fig.update_layout(
        xaxis_title="Phân khúc",
        yaxis_title="Số lượng khách hàng"
    )

    return fig


# ==========================
# TĂNG TRƯỞNG
# ==========================

def sales_growth_chart(df):

    fig = px.bar(
        df,
        x="YearMonth",
        y="Growth %",
        title="Tăng trưởng Doanh số hàng tháng (%)"
    )

    fig.update_layout(
        xaxis_title="Tháng",
        yaxis_title="Tỷ lệ tăng trưởng (%)"
    )

    return fig


def profit_growth_chart(df):

    fig = px.bar(
        df,
        x="YearMonth",
        y="Growth %",
        title="Tăng trưởng Lợi nhuận hàng tháng (%)"
    )

    fig.update_layout(
        xaxis_title="Tháng",
        yaxis_title="Tỷ lệ tăng trưởng (%)"
    )

    return fig

# ==========================
# BIỂU ĐỒ NHÓM THẤP NHẤT
# ==========================

def bottom_products_chart(df):

    fig = px.bar(
        df,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Sản phẩm có doanh số thấp nhất",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Doanh số",
        yaxis_title="Tên sản phẩm"
    )

    return fig


def bottom_profit_products_chart(df):

    fig = px.bar(
        df,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Sản phẩm có lợi nhuận thấp nhất",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Lợi nhuận",
        yaxis_title="Tên sản phẩm"
    )

    return fig


def bottom_customers_chart(df):

    fig = px.bar(
        df,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Nhóm khách hàng giá trị thấp",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Doanh số",
        yaxis_title="Tên khách hàng"
    )

    return fig


# ======================================================
# BIỂU ĐỒ PARETO
# ======================================================

def pareto_product_chart(df):

    fig = go.Figure()

    # Cột (Bar)
    fig.add_trace(
        go.Bar(
            x=df["Product Name"],
            y=df["Sales"],
            name="Doanh số"
        )
    )

    # Đường (Line)
    fig.add_trace(
        go.Scatter(
            x=df["Product Name"],
            y=df["Cumulative %"],
            mode="lines+markers",
            name="% Tích lũy",
            yaxis="y2"
        )
    )

    fig.update_layout(
        title="Phân tích Pareto - Sản phẩm",
        xaxis_title="Sản phẩm",
        yaxis=dict(
            title="Doanh số"
        ),
        yaxis2=dict(
            title="% Tích lũy",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        legend=dict(
            orientation="h"
        )
    )

    return fig


def pareto_customer_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Customer Name"],
            y=df["Sales"],
            name="Doanh số"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Customer Name"],
            y=df["Cumulative %"],
            mode="lines+markers",
            name="% Tích lũy",
            yaxis="y2"
        )
    )

    fig.update_layout(
        title="Phân tích Pareto - Khách hàng",
        xaxis_title="Khách hàng",
        yaxis=dict(
            title="Doanh số"
        ),
        yaxis2=dict(
            title="% Tích lũy",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        legend=dict(
            orientation="h"
        )
    )

    return fig

# ======================================================
# BẢN ĐỒ DOANH SỐ
# ======================================================

def sales_map_chart(df):

    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        size="Sales",
        color="Sales",
        hover_name="State/Province",
        hover_data={
            "Sales": ":,.2f",
            "Latitude": False,
            "Longitude": False
        },
        projection="natural earth",
        title="Bản đồ Phân bổ Doanh số"
    )

    fig.update_layout(
        geo=dict(
            scope="north america",
            showland=True,
            landcolor="rgb(240,240,240)",
            showcountries=True,
            countrycolor="gray"
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig


# ======================================================
# BẢN ĐỒ LỢI NHUẬN
# ======================================================

def profit_map_chart(df):

    df = df.copy()

    # Size luôn dương để biểu thị độ lớn bubble
    df["BubbleSize"] = df["Profit"].abs()

    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        size="BubbleSize",
        color="Profit",
        hover_name="State/Province",
        hover_data={
            "Profit": ":,.2f",
            "BubbleSize": False,
            "Latitude": False,
            "Longitude": False
        },
        projection="natural earth",
        title="Bản đồ Phân bổ Lợi nhuận",
        color_continuous_scale="RdYlGn" # Đỏ (lỗ) - Vàng - Xanh (lời)
    )

    fig.update_layout(
        geo=dict(
            scope="north america",
            showland=True,
            landcolor="rgb(240,240,240)",
            showcountries=True,
            countrycolor="gray"
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig