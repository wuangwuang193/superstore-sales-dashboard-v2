from src.load_data import load_data
from src.cleaning import clean_data

from src.kpi import *

from src.analysis import *

from src.visualization import *


df = load_data("data\SampleSuperstore.csv")

df = clean_data(df)


print("===== KPI =====")

print("Total Sales:", get_total_sales(df))

print("Total Profit:", get_total_profit(df))

print("Total Orders:", get_total_orders(df))

print("Total Customers:", get_total_customers(df))

print("Total Products:", get_total_products(df))

print("Total Quantity:", get_total_quantity(df))


monthly_sales = get_monthly_sales(df)

region_sales = get_sales_by_region(df)

category_sales = get_sales_by_category(df)


monthly_sales_chart(monthly_sales).show()

sales_by_region_chart(region_sales).show()

sales_by_category_chart(category_sales).show()