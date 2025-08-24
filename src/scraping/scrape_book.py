import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")
OUTPUT_PATH = "data/raw/books.csv"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    )
}

def get_book_data(book, current_url, page_num, book_num, total_books):
    """
    Scrape details for a single book from its product page.
    """
    book_link = book.select_one("a")["href"]
    full_book_url = urljoin(current_url, book_link)

    print(f"   📖 Scraping book {book_num} on page {page_num} (Total scraped: {total_books})")

    book_response = requests.get(full_book_url, headers=headers)
    book_response.raise_for_status()
    book_soup = BeautifulSoup(book_response.text, "lxml")

    # Title
    title = book_soup.find("div", class_="product_main").h1.text

    # Category
    category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

    # Price
    price = book_soup.find("p", class_="price_color").text.strip()

    # Availability
    availability_tag = book_soup.find("p", class_="instock")
    is_available = bool(availability_tag and availability_tag.find("i", class_="icon-ok"))

    # Rating
    star_tag = book_soup.find("p", class_="star-rating")
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    if star_tag:
        star_text = [cls for cls in star_tag["class"] if cls != "star-rating"][0]
        numeric_rating = rating_map.get(star_text, 0)
    else:
        numeric_rating = 0

    # Description
    desc_heading = book_soup.find("div", id="product_description")
    description = (
        desc_heading.find_next_sibling("p").text.strip()
        if desc_heading
        else "No description"
    )

    # Image
    img_tag = book_soup.find("div", class_="item active").img["src"]
    img_url = urljoin(BASE_URL, img_tag)

    return {
        "title": title,
        "category": category,
        "price": price,
        "availability": is_available,
        "rating": numeric_rating,
        "description": description,
        "img": img_url,
    }


def scrape_all_books():
    """
    Scrape all books across all pages.
    """
    all_books = []
    url = START_URL
    page_num = 1
    total_books = 0

    while True:
        print(f"\n📄 Scraping page {page_num}: {url}")
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for i, book in enumerate(books, start=1):
            try:
                book_data = get_book_data(book, url, page_num, i, total_books + 1)
                all_books.append(book_data)
                total_books += 1
            except Exception as e:
                print(f"❌ Error scraping book {i} on page {page_num}: {e}")

        # Next page
        next_page = soup.find("li", class_="next")
        if next_page:
            url = urljoin(url, next_page.find("a")["href"])
            page_num += 1
        else:
            break

    return pd.DataFrame(all_books)


if __name__ == "__main__":
    df = scrape_all_books()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"\n✅ Scraping complete! Saved {len(df)} books to {OUTPUT_PATH}")
