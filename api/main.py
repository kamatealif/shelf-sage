# api/main.py
import os
import sys
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

# ---- safe import for model (works when run from project root or as module) ----
try:
    from src.models.category_based import CategoryBasedRecommender
except Exception:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
    try:
        from src.models.category_based import CategoryBasedRecommender
    except Exception:
        # last resort: try relative src path two levels up (if running from repo root)
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
        from src.models.category_based import CategoryBasedRecommender

# ---- Config ----
BOOKS_CSV = "../data/processed/books_clean.csv"
MODEL_PKL = "models/category_based.pkl"
DEFAULT_PAGE_SIZE = 20

# ---- Pydantic schemas ----
class BookSummary(BaseModel):
    title: str
    slug: str
    category: str
    rating: Optional[int]
    price_clean: Optional[float]
    img: Optional[str]
    url: Optional[str]  # optional frontend url (constructed by frontend if needed)

class BookDetail(BookSummary):
    description: Optional[str]

class RecommendationOut(BaseModel):
    recommendations: List[BookSummary]

# ---- App setup ----
app = FastAPI(title="Book Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Helpers ----
def slugify_title(title: str) -> str:
    # simple slugify (keeps ASCII and hyphens)
    import re
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)     # remove punctuation
    s = re.sub(r"\s+", "-", s)         # spaces -> hyphens
    s = re.sub(r"-+", "-", s)          # collapse multiple hyphens
    return s

def load_books(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Books CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)
    # Ensure required columns
    for col in ["title", "category"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column in books CSV: {col}")
    # normalize title column for consistent lookup
    df["title"] = df["title"].astype(str).str.lower().str.strip()
    df["category"] = df["category"].astype(str).str.lower().str.strip()
    # create slug for safe URLs
    df["slug"] = df["title"].apply(slugify_title)
    # ensure price_clean numeric if present
    if "price_clean" in df.columns:
        df["price_clean"] = pd.to_numeric(df["price_clean"], errors="coerce")
    return df

# ---- Startup: load model & data ----
@app.on_event("startup")
def startup_event():
    global BOOKS_DF, RECOMMENDER
    # Load books
    try:
        BOOKS_DF = load_books(BOOKS_CSV)
    except Exception as e:
        # If books CSV not found, exit so developer knows
        raise RuntimeError(f"Failed to load books CSV: {e}")

    # Load or create model
    if os.path.exists(MODEL_PKL):
        RECOMMENDER = CategoryBasedRecommender.load(MODEL_PKL)
        # attach the books DataFrame in case the pickled model does not carry the df path
        # (our CategoryBasedRecommender saves the DataFrame on creation)
        RECOMMENDER.books = BOOKS_DF
        print("Loaded recommender model from pickle.")
    else:
        # If pickle missing, create and save it
        RECOMMENDER = CategoryBasedRecommender(BOOKS_DF)
        RECOMMENDER.save(MODEL_PKL)
        print("Trained and saved new recommender model.")


# ---- Endpoints ----

@app.get("/", response_model=List[BookSummary])
def list_books(page: int = Query(1, ge=1), page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=200)):
    """
    Return paginated list of all books (summary). Each item includes 'slug' that can be used with /books/{slug}.
    """
    start = (page - 1) * page_size
    end = start + page_size
    subset = BOOKS_DF.iloc[start:end]
    results = []
    for _, r in subset.iterrows():
        results.append(
            {
                "title": r["title"],
                "slug": r["slug"],
                "category": r["category"],
                "rating": int(r["rating"]) if pd.notna(r.get("rating")) else None,
                "price_clean": float(r["price_clean"]) if pd.notna(r.get("price_clean")) else None,
                "img": r.get("img"),
                "url": None,  # frontend can build full url like /books/{slug}
            }
        )
    return results


@app.get("/books/{slug}", response_model=RecommendationOut)
def get_book_and_recommendations(slug: str, top_n: int = Query(10, ge=1, le=50)):
    """
    Return book details for the slug and recommended books (from same category).
    """
    row = BOOKS_DF[BOOKS_DF["slug"] == slug]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"No book found for slug '{slug}'")

    book = row.iloc[0]
    title = book["title"]

    # get recommendations from the recommender (it expects title in lowercase)
    rec = RECOMMENDER.get_recommendations(title, top_n=top_n)
    # rec may be a dataframe or an error string
    if isinstance(rec, str):
        # error message
        raise HTTPException(status_code=404, detail=rec)

    rec_list = []
    for _, r in rec.iterrows():
        rec_list.append(
            {
                "title": r["title"],
                "slug": slugify_title(r["title"]),
                "category": r["category"],
                "rating": int(r["rating"]) if pd.notna(r.get("rating")) else None,
                "price_clean": float(r["price_clean"]) if pd.notna(r.get("price_clean")) else None,
                "img": r.get("img"),
                "url": None,
            }
        )

    # Prepare detail + recommendations; detail is the first element or separate if you need
    detail = {
        "title": book["title"],
        "slug": book["slug"],
        "category": book["category"],
        "rating": int(book["rating"]) if pd.notna(book.get("rating")) else None,
        "price_clean": float(book["price_clean"]) if pd.notna(book.get("price_clean")) else None,
        "img": book.get("img"),
        "description": book.get("description"),
        "url": None,
    }

    # Return detail inside 'recommendations' output (frontend can merge as desired)
    return {"recommendations": [detail] + rec_list}


@app.get("/categories", response_model=List[str])
def list_categories():
    """Return list of unique categories."""
    cats = sorted(BOOKS_DF["category"].dropna().unique().tolist())
    return cats


@app.get("/search", response_model=List[BookSummary])
def search_books(q: str = Query(..., min_length=1), limit: int = Query(20, ge=1, le=200)):
    """Simple case-insensitive title search."""
    q_lower = q.lower().strip()
    matched = BOOKS_DF[BOOKS_DF["title"].str.contains(q_lower, na=False)]
    matched = matched.head(limit)
    results = []
    for _, r in matched.iterrows():
        results.append(
            {
                "title": r["title"],
                "slug": r["slug"],
                "category": r["category"],
                "rating": int(r["rating"]) if pd.notna(r.get("rating")) else None,
                "price_clean": float(r["price_clean"]) if pd.notna(r.get("price_clean")) else None,
                "img": r.get("img"),
                "url": None,
            }
        )
    return results
