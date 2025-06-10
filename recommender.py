import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def recommend_similar_products(selected_product, merged_df, top_n=5):
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Fill missing values
    merged_df['name'] = merged_df['name'].fillna('')
    merged_df['category'] = merged_df['category'].fillna('')

    # Combine text features
    merged_df['text'] = merged_df['name'] + ' ' + merged_df['category']

    # Vectorize
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(merged_df['text'])

    # Find the index of the selected product
    product_idx = merged_df[merged_df['name'] == selected_product].index[0]

    # Compute similarity scores
    similarity_vector = cosine_similarity(tfidf_matrix[product_idx], tfidf_matrix).flatten()
    sim_scores = list(enumerate(similarity_vector))

    # Clean similarity scores to ensure scalar types
    cleaned_scores = []
    for i, score in sim_scores:
        if hasattr(score, "item"):
            cleaned_scores.append((i, score.item()))
        elif isinstance(score, (list, np.ndarray)) and len(score) == 1:
            cleaned_scores.append((i, float(score[0])))
        else:
            cleaned_scores.append((i, float(score)))

    # Sort by similarity, exclude the first one (same item)
    sim_scores_sorted = sorted(cleaned_scores, key=lambda x: x[1], reverse=True)[1: top_n + 1]

    # Get recommended products
    recommended = merged_df.iloc[[i for i, _ in sim_scores_sorted]]
    return recommended[['product_id', 'name', 'category']]
