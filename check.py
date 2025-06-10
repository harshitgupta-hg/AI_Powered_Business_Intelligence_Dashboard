import pandas as pd
# Load CSV files
orders_df = pd.read_csv("C:\Data\orders.csv")
products_df = pd.read_csv("C:\Data\products.csv")

# Import and use KPI generator
from kpi_generator import generate_kpis

kpis = generate_kpis(orders_df, products_df)
print(kpis)

# Continue with dashboard or visualizations...
