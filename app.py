import streamlit as st
import pandas as pd
from kpi_generator import generate_kpis
import plotly.express as px
import numpy as np
from sklearn.ensemble import IsolationForest


st.set_page_config(page_title="Business Intelligence Dashboard", layout="centered")

st.title("📊 Business Intelligence KPI Dashboard")

st.sidebar.header("📂 Upload CSV Files")

orders_file = st.sidebar.file_uploader("Upload Orders CSV", type=["csv"])
products_file = st.sidebar.file_uploader("Upload Products CSV", type=["csv"])

if orders_file is not None and products_file is not None:
    orders_df = pd.read_csv(orders_file)
    products_df = pd.read_csv(products_file)
    
    # Merge only when both are loaded
    merged_df = pd.merge(orders_df, products_df, on='product_id')
else:
    st.warning("Please upload both Orders and Products CSV files to proceed.")


if orders_file and products_file:
    try:
        orders_df = pd.read_csv("C:\Data\orders.csv")
        products_df = pd.read_csv("C:\Data\products.csv")

        kpis = generate_kpis(orders_df, products_df)

        st.subheader("📌 KPIs")
        for kpi_name, kpi_value in kpis.items():
            st.metric(label=kpi_name, value=kpi_value)

        # Export option
        if st.button("Download KPI Summary as CSV"):
            kpi_df = pd.DataFrame(kpis.items(), columns=["KPI", "Value"])
            csv = kpi_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name='kpi_summary.csv',
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"Error processing files: {e}")
else:
    st.info("To get detailed KPIs please upload both Orders and Products CSV files to continue.")
    

# Set the Streamlit app title
st.title("📊 AI-Powered BI Dashboard")

# Load your datasets
orders_df = pd.read_csv("C:\Data\orders.csv")
products_df = pd.read_csv("C:\Data\products.csv")

# Merge to get price from products
merged_df = pd.merge(orders_df, products_df, on="product_id")

# Calculate revenue
merged_df["revenue"] = merged_df["quantity"] * merged_df["price"]

# Convert order_date to datetime
merged_df["order_date"] = pd.to_datetime(merged_df["order_date"])

# Extract month from order date
merged_df["month"] = merged_df["order_date"].dt.to_period("M").astype(str)

# Group by month to get total revenue
monthly_revenue = merged_df.groupby("month")["revenue"].sum().reset_index()

# Debugging (optional)
# st.dataframe(monthly_revenue.head())

# Plot revenue chart
st.subheader("📈 Monthly Revenue Trend")
fig = px.line(
    monthly_revenue,
    x="month",
    y="revenue",
    title="Monthly Revenue Over Time",
    markers=True
)
st.plotly_chart(fig)

# Group by category to get revenue per category
category_revenue = merged_df.groupby("category")["revenue"].sum().reset_index().sort_values(by="revenue", ascending=False)

# Plot Top Categories by Revenue
st.subheader("🏆 Top Categories by Revenue")
fig2 = px.bar(
    category_revenue,
    x="category",
    y="revenue",
    title="Revenue by Product Category",
    color="category",
    text_auto='.2s'
)
st.plotly_chart(fig2)

st.subheader("🤖 Smart Product Recommendations")

# Top 5 Selling Products
top_products = (
    merged_df.groupby("name")["quantity"]
    .sum()
    .reset_index()
    .sort_values(by="quantity", ascending=False)
    .head(5)
)

st.markdown("**🔥 Top 5 Best-Selling Products:**")
for i, row in top_products.iterrows():
    st.write(f"➡️ {row['name']} (Sold: {int(row['quantity'])})")

# Bottom 5 Selling Products
bottom_products = (
    merged_df.groupby("name")["quantity"]
    .sum()
    .reset_index()
    .sort_values(by="quantity", ascending=True)
    .head(5)
)

st.markdown("**🧊 Consider Promoting These Low-Sellers:**")
for i, row in bottom_products.iterrows():
    st.write(f"⚠️ {row['name']} (Sold: {int(row['quantity'])})")



# --- Anomaly Detection ---
st.subheader("📉 Anomaly Detection: Revenue Drops")

# Ensure order_date is datetime
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])

# Step 1: Daily Revenue Summary
daily_revenue = merged_df.groupby('order_date')['revenue'].sum().reset_index()

# Step 2: Detect anomalies
model = IsolationForest(contamination=0.05, random_state=42)
daily_revenue['anomaly'] = model.fit_predict(daily_revenue[['revenue']])
daily_revenue['is_anomaly'] = daily_revenue['anomaly'] == -1

# Step 3: Plot
fig = px.line(daily_revenue, x='order_date', y='revenue', title='Revenue Over Time with Anomalies')
fig.add_scatter(
    x=daily_revenue[daily_revenue['is_anomaly']]['order_date'],
    y=daily_revenue[daily_revenue['is_anomaly']]['revenue'],
    mode='markers',
    name='Anomaly',
    marker=dict(color='red', size=10)
)

st.plotly_chart(fig)


from recommender import recommend_similar_products

st.subheader("🔎 Product Recommendations")

# Dropdown for product selection
selected_product = st.selectbox("Select a product to get similar recommendations:", merged_df["name"].unique())

similar_products = recommend_similar_products(selected_product, merged_df)
st.write(similar_products)

# Show similar product recommendations
if selected_product:
    similar_products = recommend_similar_products(selected_product, merged_df)
    st.write("✅ Recommended Products:", similar_products)

st.subheader("⬇️ Download Processed Data")

csv_data = merged_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Merged Data as CSV",
    data=csv_data,
    file_name='merged_data.csv',
    mime='text/csv'
)

from nl_query import run_local_llm_query

# Add a text input for natural language question
user_query = st.text_input("Ask a question about your data:")

if user_query:
    response = run_local_llm_query(user_query, orders_df, products_df)
    st.subheader("🤖 LLM Response")
    st.write(response)

st.markdown("---")
st.caption("⚡ Powered by Harshit Gupta's code ⚡(https://github.com/harshitgupta-hg)")
