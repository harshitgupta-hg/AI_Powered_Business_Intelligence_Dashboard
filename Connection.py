import pandas as pd
from sqlalchemy import create_engine

# Update with your actual credentials
user = "admin"
password = "admin123"
host = "localhost"
port = "5432"
database = "bi_dashboard"

# Create connection string
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

# Test: Load customers table
df_customers = pd.read_sql("SELECT * FROM customers", engine)
print(df_customers.head())
