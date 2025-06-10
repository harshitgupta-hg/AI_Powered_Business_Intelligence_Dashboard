from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

# 1. Customers Table
def generate_customers(n=500):
    customers = []
    for i in range(1, n + 1):
        customers.append({
            'customer_id': i,
            'name': fake.name(),
            'email': fake.email(),
            'gender': random.choice(['Male', 'Female']),
            'age': random.randint(18, 60),
            'location': fake.city(),
            'signup_date': fake.date_between(start_date='-2y', end_date='today')
        })
    return pd.DataFrame(customers)

# 2. Products Table
def generate_products(n=100):
    categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Sports']
    products = []
    for i in range(1, n + 1):
        category = random.choice(categories)
        products.append({
            'product_id': i,
            'name': fake.word().capitalize(),
            'category': category,
            'price': round(random.uniform(10, 500), 2)
        })
    return pd.DataFrame(products)

# 3. Orders Table
def generate_orders(customers_df, products_df, n=1500):
    orders = []
    for i in range(1, n + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        orders.append({
            'order_id': i,
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'quantity': random.randint(1, 5),
            'order_date': fake.date_between(start_date=customer['signup_date'], end_date='today')
        })
    return pd.DataFrame(orders)

# 4. Feedback Table
def generate_feedback(customers_df, products_df, n=500):
    feedback = []
    for i in range(1, n + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        feedback.append({
            'feedback_id': i,
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'rating': random.randint(1, 5),
            'comment': fake.sentence()
        })
    return pd.DataFrame(feedback)

# Generate DataFrames
customers_df = generate_customers()
products_df = generate_products()
orders_df = generate_orders(customers_df, products_df)
feedback_df = generate_feedback(customers_df, products_df)

# Save to CSV
customers_df.to_csv('customers.csv', index=False)
products_df.to_csv('products.csv', index=False)
orders_df.to_csv('orders.csv', index=False)
feedback_df.to_csv('feedback.csv', index=False)

print("✅ CSV files generated successfully!")
