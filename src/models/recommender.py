import os
import sys
import pandas as pd

try:
    from src.models.category_based import CategoryBasedRecommender
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.models.category_based import CategoryBasedRecommender


MODEL_PATH = "models/category_based.pkl"


class BookRecommender:
    def __init__(self, books_path: str, retrain: bool = False):
        """
        Wrapper for Category-Based Recommender.
        """
        if os.path.exists(MODEL_PATH) and not retrain:
            self.model = CategoryBasedRecommender.load(MODEL_PATH)
        else:
            books = pd.read_csv(books_path)
            print(f"✅ Loaded {len(books)} books.")
            self.model = CategoryBasedRecommender(books)
            self.model.save(MODEL_PATH)

    def recommend(self, title: str, top_n: int = 10):
        return self.model.get_recommendations(title, top_n)


if __name__ == "__main__":
    books_path = "data/processed/books_clean.csv"

    if not os.path.exists(books_path):
        print(f"❌ Dataset not found at {books_path}")
        sys.exit(1)

    recommender = BookRecommender(books_path, retrain=True)

    query = input("\n📖 Enter a book title: ").strip().lower()
    print(f"\n🔍 Recommendations for '{query}':")
    print(recommender.recommend(query, top_n=10))
