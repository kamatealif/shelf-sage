# src/models/recommender.py

import os
import sys
import pandas as pd

# 🔹 Handle imports (works as script & module)
try:
    # If running as part of package
    from src.models.content_based import ContentBasedRecommender
except ModuleNotFoundError:
    # If running directly (fallback: add project root to sys.path)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.models.content_based import ContentBasedRecommender


class BookRecommender:
    def __init__(self, books_path: str):
        """
        Wrapper class for book recommendation.
        Args:
            books_path (str): Path to processed books CSV.
        """
        self.books = pd.read_csv(books_path)
        print(f"✅ Loaded {len(self.books)} books.")

        # Initialize content-based recommender
        self.model = ContentBasedRecommender(self.books)

    def recommend(self, title: str, top_n: int = 5):
        """
        Get recommendations for a given book title.
        """
        return self.model.get_similar_books(title, top_n)


if __name__ == "__main__":
    # Example usage when run directly
    books_path = "data/processed/books_clean.csv"

    if not os.path.exists(books_path):
        print(f"❌ Dataset not found at {books_path}")
        sys.exit(1)

    recommender = BookRecommender(books_path)

    query ="tipping the velvet"  # change this to test with other books
    print(f"\n🔍 Recommendations for '{query}':")
    print(recommender.recommend(query, top_n=5))
