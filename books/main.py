import requests
from bs4 import BeautifulSoup 
import pandas as pd

Book_names = []
Book_images = []
Book_prices = []
Book_Availability = []

url = "https://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

book_containers = soup.find_all("article", class_="product_pod")

for book in book_containers:
    # Book image 
    img_src = book.find("img")["src"]
    full_img_url = "https://books.toscrape.com/" + img_src.replace("../", "")
    Book_images.append(full_img_url)

    # Book name
    book_name = book.find("h3").find("a").get("title")
    Book_names.append(book_name)

    # Book price
    book_price = book.find("p", class_="price_color").text
    Book_prices.append(book_price)

    # Book availability
    availability = book.find("p", class_="instock availability").text.strip()
    Book_Availability.append(availability)

data_frame = pd.DataFrame({
    "book_name": Book_names,
    "price": Book_prices,
    "availability": Book_Availability,
    "image": Book_images
})

data_frame.to_json("books.json", orient="records", indent=2)
print("books.json created successfully.")
