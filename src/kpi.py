def get_total_sales(df):
    return df["Sales"].sum()


def get_total_profit(df):
    return df["Profit"].sum()


def get_total_orders(df):
    return df["Order ID"].nunique()


def get_total_customers(df):
    return df["Customer ID"].nunique()


def get_total_products(df):
    return df["Product ID"].nunique()


def get_total_quantity(df):
    return df["Quantity"].sum()

def get_sales_growth_rate(df):

    monthly_sales = (
        df.groupby("YearMonth")["Sales"]
        .sum()
    )

    growth = monthly_sales.pct_change()

    return growth.iloc[-1] * 100

def get_profit_growth_rate(df):

    monthly_profit = (
        df.groupby("YearMonth")["Profit"]
        .sum()
    )

    growth = monthly_profit.pct_change()

    return growth.iloc[-1] * 100

def get_sales_growth_rate(df):

    monthly_sales = (
        df.groupby("YearMonth")["Sales"]
        .sum()
        .reset_index()
    )

    if len(monthly_sales) < 2:
        return 0

    current = monthly_sales.iloc[-1]["Sales"]
    previous = monthly_sales.iloc[-2]["Sales"]

    if previous == 0:
        return 0

    growth = (
        (current - previous)
        / previous
    ) * 100

    return growth


def get_profit_growth_rate(df):

    monthly_profit = (
        df.groupby("YearMonth")["Profit"]
        .sum()
        .reset_index()
    )

    if len(monthly_profit) < 2:
        return 0

    current = monthly_profit.iloc[-1]["Profit"]
    previous = monthly_profit.iloc[-2]["Profit"]

    if previous == 0:
        return 0

    growth = (
        (current - previous)
        / previous
    ) * 100

    return growth