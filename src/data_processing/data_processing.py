# src/data_processing.py

import pandas as pd
import re
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the books dataset from a CSV file.
    """
    try:
        books = pd.read_csv(file_path)
        print(f" Loaded dataset with {len(books)} books and {len(books.columns)} columns.")
        return books
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Failed to parse file {file_path}.")
        return None


def clean_price(price: str) -> float:
    """
    Clean price string (£51.77) -> 51.77 as float.
    """
    try:
        return float(re.sub(r"[^\d.]", "", str(price)))
    except ValueError:
        return None


def preprocess_books(books: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the books dataframe:
    - Clean price column
    - Normalize text columns (title, category)
    - Handle missing values
    """
    if books is None:
        return None

    books = books.copy()

    # Clean price
    if "price" in books.columns:
        books["price_clean"] = books["price"].apply(clean_price)
        print(" Cleaned 'price' column into 'price_clean'.")
    
    # Normalize text columns
    for col in ["title", "category"]:
        if col in books.columns:
            books[col] = books[col].astype(str).str.lower().str.strip()
            print(f" Normalized text column: {col}")
    
    # Handle missing values
    books.fillna({"title": "unknown", "category": "unknown"}, inplace=True)

    print(f" Preprocessing complete. Final shape: {books.shape}")
    return books


def save_processed_data(books: pd.DataFrame, output_path: str):
    """
    Save the cleaned/preprocessed dataset to a new CSV file.
    """
    if books is not None:
        books.to_csv(output_path, index=False)
        print(f" Saved processed dataset to {output_path}")


if __name__ == "__main__":
    # Example usage
    raw_path = "../../data/raw/books.csv"         # your scraped dataset
    processed_path = "../../data/processed/books_clean.csv"

    # Create the directory if it doesn't exist
    processed_dir = os.path.dirname(processed_path)
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    books = load_data(raw_path)
    if books is not None:
        books = preprocess_books(books)
        save_processed_data(books, processed_path)

    print(" Data processing complete!")