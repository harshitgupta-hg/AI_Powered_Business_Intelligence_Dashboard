import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_query(nl_query):
    nl_query = nl_query.lower()

    if "total revenue last month" in nl_query:
        return """SELECT SUM(revenue) 
                  FROM sales_data 
                  WHERE sale_date >= date_trunc('month', current_date - interval '1 month') 
                  AND sale_date < date_trunc('month', current_date);"""

    elif "top 5 products" in nl_query:
        return """SELECT product_name, SUM(quantity) as total_sold 
                  FROM sales_data 
                  GROUP BY product_name 
                  ORDER BY total_sold DESC 
                  LIMIT 5;"""
    
    # Add more patterns as needed

    return "Sorry, I couldn't understand the query."

# Example usage
query = input("Ask a question: ")
print(parse_query(query))
