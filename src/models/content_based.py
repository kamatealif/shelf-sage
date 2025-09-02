
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    def __init__(self, books: pd.DataFrame):
        """
        Content-based recommender using TF-IDF + cosine similarity.
        Args:
            books (pd.DataFrame): DataFrame containing at least 'title' and 'category'.
        """
        self.books = books.copy()

        # Combine features (title + category + description)
        self.books["features"] = (
            self.books["title"].astype(str)
            + " "
            + self.books["category"].astype(str)
            + " "
            + self.books["description"].astype(str)
        )

        # Vectorize text data
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.books["features"])

        # Compute similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        print("📊 TF-IDF and similarity matrix created.")

    def get_similar_books(self, title: str, top_n: int = 5):
        """
        Recommend similar books based on title.
        """
        title = title.lower().strip()

        # Check if book exists
        if title not in self.books["title"].values:
            return f"❌ Book '{title}' not found in dataset."

        # Get index of the book
        idx = self.books[self.books["title"] == title].index[0]

        # Get similarity scores for this book
        sim_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort by similarity (skip first = same book)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1 : top_n + 1]

        # Get recommended books
        recommendations = self.books.iloc[[i[0] for i in sim_scores]][
            ["title", "category", "rating", "price_clean"]
        ]

        return recommendations.reset_index(drop=True)
