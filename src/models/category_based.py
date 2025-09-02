# src/models/category_based.py

import pandas as pd

class CategoryBasedRecommender:
    def __init__(self, books: pd.DataFrame):
        self.books = books.copy()

    def get_recommendations(self, title: str, top_n: int = 5):
        """
        Recommend books from the same category as the input book.
        """
        title = title.lower().strip()

        # Check if the book exists
        if title not in self.books["title"].values:
            return f"❌ Book '{title}' not found in dataset."

        # Get category of the input book
        category = self.books.loc[self.books["title"] == title, "category"].values[0]
        print(f"📂 Category for '{title}': {category}")

        # Get all books in same category (excluding the input book itself)
        similar_books = self.books[
            (self.books["category"] == category) & (self.books["title"] != title)
        ]

        # Sort by rating (descending) then price (ascending)
        similar_books = similar_books.sort_values(
            by=["rating", "price_clean"], ascending=[False, True]
        )

        return similar_books.head(top_n)[["title", "category", "rating", "price_clean"]]
