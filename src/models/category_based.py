import os
import pickle
import pandas as pd


class CategoryBasedRecommender:
    def __init__(self, books: pd.DataFrame):
        """
        Category-based recommender.
        Args:
            books (pd.DataFrame): DataFrame with columns: title, category, rating, price_clean
        """
        self.books = books.copy()

    def get_recommendations(self, title: str, top_n: int = 10):
        """
        Recommend books from the same category as the input book.
        Args:
            title (str): Book title (must exist in dataset)
            top_n (int): Number of recommendations
        Returns:
            pd.DataFrame: Recommended books
        """
        title = title.lower().strip()

        # Ensure book exists
        if title not in self.books["title"].values:
            return f"❌ Book '{title}' not found in dataset."

        # Get category of the input book
        category = self.books.loc[self.books["title"] == title, "category"].values[0]
        print(f"📂 Category for '{title}': {category}")

        # Get other books in the same category
        similar_books = self.books[
            (self.books["category"] == category) & (self.books["title"] != title)
        ]

        # Sort: higher rating first, then lower price
        similar_books = similar_books.sort_values(
            by=["rating", "price_clean"], ascending=[False, True]
        )

        return similar_books.head(top_n)[["title", "category", "rating", "price_clean"]]

    def save(self, filepath: str):
        """
        Save the trained recommender to a pickle file.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)  # ensure folder exists
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        print(f"💾 Model saved to {filepath}")

    @staticmethod
    def load(filepath: str):
        """
        Load a recommender from a pickle file.
        """
        with open(filepath, "rb") as f:
            model = pickle.load(f)
        print(f"✅ Model loaded from {filepath}")
        return model
