import subprocess
import psycopg2

# ---- DB CONFIG ----
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'admin',
    'password': 'admin123',
    'host': 'localhost',
    'port': '5432',
}

# ---- RULE-BASED PARSER ----
def rule_based_parser(nl_query):
    q = nl_query.lower()

    if "total revenue last month" in q:
        return """SELECT SUM(revenue) AS total_revenue
FROM sales_data
WHERE sale_date >= date_trunc('month', current_date - interval '1 month')
AND sale_date < date_trunc('month', current_date);"""

    elif "top 5 products" in q:
        return """SELECT product_name, SUM(quantity) AS total_sold
FROM sales_data
GROUP BY product_name
ORDER BY total_sold DESC
LIMIT 5;"""

    elif "total customers" in q:
        return """SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM sales_data;"""

    return None


# ---- OLLAMA FALLBACK ----
def ask_ollama(prompt):
    full_prompt = f"Convert this to a PostgreSQL SQL query. The table is 'sales_data': {prompt}"

    try:
        command = ['ollama', 'run', 'llama3']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=full_prompt)
        return stdout.strip()
    except Exception as e:
        return f"-- Ollama Error: {e}"


# ---- EXECUTE SQL ----
def run_sql_query(sql):
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                try:
                    rows = cur.fetchall()
                    columns = [desc[0] for desc in cur.description]
                    print("\n📊 Query Results:\n")
                    print(columns)
                    for row in rows:
                        print(row)
                except psycopg2.ProgrammingError:
                    print("\n✅ Query executed (no data returned)")
    except Exception as e:
        print(f"❌ DB Error: {e}")


# ---- MAIN APP ----
def main():
    nl_query = input("\nAsk your question: ")

    sql = rule_based_parser(nl_query)

    if sql:
        print("\n✅ Rule-Based SQL Generated:\n", sql)
    else:
        print("\n🤖 Using LLaMA 3 (Ollama)...")
        sql = ask_ollama(nl_query)
        print("\n🧠 LLaMA 3 SQL Output:\n", sql)

    # Confirm and run
    confirm = input("\n▶️ Run this query? (y/n): ").lower()
    if confirm == 'y':
        run_sql_query(sql)


if __name__ == "__main__":
    main()
