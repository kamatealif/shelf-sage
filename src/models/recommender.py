# src/models/recommender.py

import os
import sys
import pandas as pd

try:
    from src.models.category_based import CategoryBasedRecommender
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.models.category_based import CategoryBasedRecommender


class BookRecommender:
    def __init__(self, books_path: str):
        self.books = pd.read_csv(books_path)
        print(f"✅ Loaded {len(self.books)} books.")
        self.model = CategoryBasedRecommender(self.books)

    def recommend(self, title: str, top_n: int = 5):
        return self.model.get_recommendations(title, top_n)


if __name__ == "__main__":
    books_path = "data/processed/books_clean.csv"

    if not os.path.exists(books_path):
        print(f"❌ Dataset not found at {books_path}")
        sys.exit(1)

    recommender = BookRecommender(books_path)
    print("\n📚 Welcome to the Book Recommender!")
    print("🔍 search only for book that we have available in our books.csv")
    query = input("\n📖 Enter a book title: ").strip().lower()
    print(f"\n🔍 Recommendations for '{query}':")
    print(recommender.recommend(query, top_n=5))

    print("\n👋 Goodbye!")