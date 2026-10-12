import pandas as pd
from src.map_data import STATE_LOCATION
# ======================================================
# US STATE CODE
# ======================================================

STATE_CODE = {
    "Alabama": "AL",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}



# ==========================
# Monthly Sales
# ==========================
def get_monthly_sales(df):

    return (
        df.groupby("YearMonth", as_index=False)["Sales"]
        .sum()
    )


# ==========================
# Yearly Sales
# ==========================
def get_yearly_sales(df):

    return (
        df.groupby("Year", as_index=False)["Sales"]
        .sum()
    )


# ==========================
# Sales by Region
# ==========================
def get_sales_by_region(df):

    return (
        df.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


# ==========================
# Sales by Category
# ==========================
def get_sales_by_category(df):

    return (
        df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


# ==========================
# Sales by State
# ==========================
def get_sales_by_state(df):

    column = "State/Province" if "State/Province" in df.columns else "State"

    return (
        df.groupby(column, as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


# ==========================
# Sales by City
# ==========================
def get_sales_by_city(df):

    return (
        df.groupby("City", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


# ==========================
# Top Products
# ==========================
def get_top_products(df, top_n=10):

    return (
        df.groupby("Product Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(top_n)
    )


# ==========================
# Top Customers
# ==========================
def get_top_customers(df, top_n=10):

    return (
        df.groupby("Customer Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(top_n)
    )


# ==========================
# Top Sub Category
# ==========================
def get_top_subcategory(df):

    return (
        df.groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

# ==========================
# Monthly Profit
# ==========================
def get_monthly_profit(df):

    return (
        df.groupby("YearMonth", as_index=False)["Profit"]
        .sum()
    )


# ==========================
# Profit by Region
# ==========================
def get_profit_by_region(df):

    return (
        df.groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )


# ==========================
# Profit by Category
# ==========================
def get_profit_by_category(df):

    return (
        df.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )


# ==========================
# Top Products by Profit
# ==========================
def get_top_profit_products(df):

    return (
        df.groupby("Product Name", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
        .head(10)
    )

def get_quantity_by_category(df):

    return (
        df.groupby("Category", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
    )


def get_quantity_by_region(df):

    return (
        df.groupby("Region", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
    )


def get_quantity_by_subcategory(df):

    return (
        df.groupby("Sub-Category", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
    )
def get_sales_by_segment(df):

    return (
        df.groupby("Segment", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


def get_customer_count_by_segment(df):

    return (
        df.groupby("Segment")["Customer ID"]
        .nunique()
        .reset_index(name="Customers")
        .sort_values("Customers", ascending=False)
    )

def get_sales_growth(df):

    monthly_sales = (
        df.groupby("YearMonth")["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Growth %"] = (
        monthly_sales["Sales"]
        .pct_change() * 100
    )

    return monthly_sales

def get_profit_growth(df):

    monthly_profit = (
        df.groupby("YearMonth")["Profit"]
        .sum()
        .reset_index()
    )

    monthly_profit["Growth %"] = (
        monthly_profit["Profit"]
        .pct_change() * 100
    )

    return monthly_profit

def get_best_region(df):

    region = (
        df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
        .sort_values(
            by="Profit",
            ascending=False
        )
    )

    return region.iloc[0]


def get_best_category(df):

    category = (
        df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
        .sort_values(
            by="Profit",
            ascending=False
        )
    )

    return category.iloc[0]

def get_bottom_products(df, top_n=10):

    return (
        df.groupby("Product Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Sales",
            ascending=True
        )
        .head(top_n)
    )


def get_bottom_profit_products(df, top_n=10):

    return (
        df.groupby("Product Name")["Profit"]
        .sum()
        .reset_index()
        .sort_values(
            by="Profit",
            ascending=True
        )
        .head(top_n)
    )


def get_bottom_customers(df, top_n=10):

    return (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Sales",
            ascending=True
        )
        .head(top_n)
    )

# ======================================================
# PARETO ANALYSIS
# ======================================================

def get_product_pareto(df):

    pareto = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
    )

    pareto["Cumulative Sales"] = pareto["Sales"].cumsum()

    total_sales = pareto["Sales"].sum()

    pareto["Cumulative %"] = (
        pareto["Cumulative Sales"] / total_sales
    ) * 100

    return pareto


def get_customer_pareto(df):

    pareto = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
    )

    pareto["Cumulative Sales"] = pareto["Sales"].cumsum()

    total_sales = pareto["Sales"].sum()

    pareto["Cumulative %"] = (
        pareto["Cumulative Sales"] / total_sales
    ) * 100

    return pareto

# ======================================================
# MAP ANALYSIS
# ======================================================

def get_sales_map(df):

    sales = (
        df.groupby("State/Province")["Sales"]
        .sum()
        .reset_index()
    )

    sales["Latitude"] = sales["State/Province"].apply(
        lambda x: STATE_LOCATION.get(x, (None, None))[0]
    )

    sales["Longitude"] = sales["State/Province"].apply(
        lambda x: STATE_LOCATION.get(x, (None, None))[1]
    )

    return sales


def get_profit_map(df):

    profit = (
        df.groupby("State/Province")["Profit"]
        .sum()
        .reset_index()
    )

    profit["Latitude"] = profit["State/Province"].apply(
        lambda x: STATE_LOCATION.get(x, (None, None))[0]
    )

    profit["Longitude"] = profit["State/Province"].apply(
        lambda x: STATE_LOCATION.get(x, (None, None))[1]
    )

    return profit
# ======================================================
# DECISION SUPPORT SYSTEM
# ======================================================

def recommend_region(df):
    region = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .iloc[0]
    )

    return {
        "ket_qua": region["Region"],
        "ly_do": [
            "Doanh thu cao nhất.",
            "Tiềm năng mở rộng thị trường.",
            "Nên ưu tiên đầu tư Marketing."
        ],
        "khuyen_nghi": f"Nên tăng đầu tư tại khu vực {region['Region']}."
    }


def recommend_category(df):
    category = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .iloc[0]
    )

    return {
        "ket_qua": category["Category"],
        "ly_do": [
            "Lợi nhuận cao nhất.",
            "Hiệu quả kinh doanh tốt.",
            "Mang lại giá trị cao."
        ],
        "khuyen_nghi": f"Nên đẩy mạnh danh mục {category['Category']}."
    }


def recommend_product(df):
    product = (
        df.groupby("Product Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values(["Profit", "Sales"])
        .iloc[0]
    )

    return {
        "ket_qua": product["Product Name"],
        "ly_do": [
            "Lợi nhuận thấp.",
            "Hiệu quả kinh doanh kém.",
            "Cần xem xét lại."
        ],
        "khuyen_nghi": "Xem xét giảm kinh doanh hoặc loại bỏ sản phẩm này."
    }


def recommend_customer(df):
    customer = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .iloc[0]
    )

    return {
        "ket_qua": customer["Customer Name"],
        "ly_do": [
            "Mang lại doanh thu cao nhất.",
            "Là khách hàng giá trị.",
            "Có tiềm năng mua hàng lâu dài."
        ],
        "khuyen_nghi": "Nên triển khai chương trình khách hàng VIP."
    }


def recommend_risk_region(df):
    region = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values()
        .reset_index()
        .iloc[0]
    )

    return {
        "ket_qua": region["Region"],
        "ly_do": [
            "Lợi nhuận thấp nhất.",
            "Có nguy cơ hoạt động kém hiệu quả.",
            "Cần rà soát chiến lược bán hàng."
        ],
        "khuyen_nghi": f"Nên phân tích nguyên nhân lợi nhuận thấp tại khu vực {region['Region']}."
    }