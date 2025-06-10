import pandas as pd
import matplotlib.pyplot as plt

# Load order data
orders = pd.read_csv("orders.csv")
products = pd.read_csv("products.csv")

# Merge orders with product prices
data = orders.merge(products, on="product_id")

# Group by order date and calculate total revenue
daily_revenue = data.groupby("order_date")["price"].sum().reset_index()
daily_revenue.columns = ["date", "revenue"]
daily_revenue["date"] = pd.to_datetime(daily_revenue["date"])

# Sort by date
daily_revenue = daily_revenue.sort_values("date")

# Add a 7-day rolling average
daily_revenue["rolling_mean"] = daily_revenue["revenue"].rolling(window=7).mean()

# Detect anomalies: Revenue drop > 20% from average
daily_revenue["is_anomaly"] = daily_revenue["revenue"] < (daily_revenue["rolling_mean"] * 0.8)

# Save anomalies to file
anomalies = daily_revenue[daily_revenue["is_anomaly"]]
anomalies.to_csv("revenue_anomalies.csv", index=False)

# Plot revenue with anomaly markers
plt.figure(figsize=(12,6))
plt.plot(daily_revenue["date"], daily_revenue["revenue"], label="Revenue")
plt.plot(daily_revenue["date"], daily_revenue["rolling_mean"], label="7-Day Avg", linestyle="--")

# Plot anomalies
plt.scatter(anomalies["date"], anomalies["revenue"], color="red", label="Anomalies", zorder=5)
plt.title("Daily Revenue with Anomaly Detection")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
