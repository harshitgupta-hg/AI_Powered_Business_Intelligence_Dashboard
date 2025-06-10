import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data
orders = pd.read_csv("orders.csv")
products = pd.read_csv("products.csv")
customers = pd.read_csv("customers.csv")

# Merge data
data = orders.merge(products, on="product_id").merge(customers, on="customer_id")

# Create customer-product matrix
matrix = pd.pivot_table(data, index="customer_id", columns="product_id", values="quantity", aggfunc="sum", fill_value=0)

# Compute cosine similarity
similarity = cosine_similarity(matrix)
similarity_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

# Recommend function
def recommend_for(customer_id, top_n=3):
    sim_scores = similarity_df[customer_id].sort_values(ascending=False)[1:]
    top_customers = sim_scores.head(3).index
    recommended = matrix.loc[top_customers].sum(axis=0)
    customer_products = matrix.loc[customer_id]
    recommended = recommended[customer_products == 0]
    top_recommend = recommended.sort_values(ascending=False).head(top_n).index.tolist()
    return products[products["product_id"].isin(top_recommend)][["product_id", "name", "price"]]

# Example usage
print("Recommendations for Customer ID 2:")
print(recommend_for(customer_id=2))
