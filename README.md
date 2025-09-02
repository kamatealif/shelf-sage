
# 📚 Book Recommendation Engine

A full-stack **Book Recommendation System** built from scratch with Python.  
i scrape book data, clean it, analyze it (EDA), and train a **content-based recommender** using TF-IDF and Cosine Similarity.  
Later, i'll expose it through an API, build a frontend, and deploy it with CI/CD pipelines. 🚀

<div style={{ display: "flex", gap: "8px", marginTop: "10px" }}>
  Python
  Data Science
  Machine Learning
  In Progress
</div>

---

## ✨ Features (So Far)

- ✅ Web scraping from [Books to Scrape](https://books.toscrape.com) (1000 books).  
- ✅ Cleaned & preprocessed dataset (`books_clean.csv`).  
- ✅ Exploratory Data Analysis (EDA): categories, price distribution, ratings, word clouds.  
- ✅ Content-Based Recommendation Model (TF-IDF + Cosine Similarity).  
- ✅ Robust `BookRecommender` class for reuse in scripts and notebooks.  

---

## 📂 Project Structure

```bash
book-recommender/
├── data/
│   ├── raw/                # Scraped raw data
│   ├── processed/          # Cleaned data
│   └── books.csv           # Original scraped dataset
│
├── notebooks/              # Jupyter experiments
│   ├── 01_scraping_demo.ipynb
│   ├── 02_eda.ipynb
│   └── 03_recommendation_demo.ipynb
│
├── src/
│   ├── scraping/           # Web scraping code
│   │   └── scrape_books.py
│   ├── preprocessing/      # Data cleaning
│   │   └── clean_data.py
│   ├── models/             # ML models
│   │   ├── __init__.py
│   │   ├── content_based.py
│   │   └── recommender.py
│   └── utils/              # Helper utilities
│
├── tests/                  # Unit tests (coming soon)
├── api/                    # API (future step)
├── frontend/               # Frontend (future step)
├── requirements.txt
└── README.mdx

```

---

### ⚡ Quick Start

1. Clone the repo

```bash
git clone https://github.com/kamatealif/shelf-sage.git
cd shelf-sage
```

2. Create & activate a virtual environment(i am using uv)

```bash
# to install the uv if not installed
pip install uv

# to create the .venv with dependecines installed in it
uv sync

# activate it 
.\.venv\Scripts\activate
```

3. Scrape the dataset

```bash
python src/scraping/scrape_books.py
```

4. Preprocess the data

```bash
python src/preprocessing/clean_data.py
```

5. Run the recommender

```bash
python src/models/recommender.py
```

---

🧠 How It Works

- TF-IDF Vectorizer converts text (title + category + description) into numbers.

- Cosine Similarity measures how close two books are in that space.

- The recommender returns the most similar books for a given title.

---
🛠️ Tech Stack

- Python (data scraping, processing, ML)

- BeautifulSoup (scraping)

- Pandas / NumPy (data wrangling)

- Matplotlib / Seaborn / WordCloud (EDA)

- scikit-learn (TF-IDF, cosine similarity)

- FastAPI (planned, backend API)

- svelte/Streamlit (planned, frontend UI)

- Docker + GitHub Actions (planned, deployment & CI/CD)

---
👨‍💻 Author

Your Name (@[kamatealif](kamatealif.github.io))
