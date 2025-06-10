def run_local_llm_query(user_query, orders_df, products_df):
    import ollama

    # Create the prompt manually
    prompt = (
        "You are an intelligent assistant. Here is a snapshot of the data.\n\n"
        "Orders Data:\n"
        + orders_df.head(5).to_string()
        + "\n\nProducts Data:\n"
        + products_df.head(5).to_string()
        + f"\n\nUser Question: {user_query}\n"
        "Answer based on the data above in a concise way."
    )

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={"timeout": 20},
        )
        return response['message']['content']
    except Exception as e:
        return f"⏰ LLM query failed: {e}"
