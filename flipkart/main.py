import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

Product_name = []
Prices = []
Description = []
Reviews = []
Images = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

for i in range(2, 3):
    url = f"https://www.flipkart.com/search?q=mobiles+under+15000+5g&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=mobiles+under+15000+5g%7CMobiles&requestId=e9c75a2c-95a7-4b8c-b085-23c59472211b&as-backfill=on&page={i}"

    r = requests.get(url, headers=headers)
    print(r)
    if r.status_code != 200:
        print("Skipping due to rate limit or error.")
        time.sleep(5) 
        continue

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_ = "DOjaWF gdgoEp")

    names = box.find_all("div", class_ = "KzDlHZ")

    for i in names:
        name =  i.text
        Product_name.append(name)

    # print(Product_name)

    prices = box.find_all("div", class_= "Nx9bqj _4b5DiR")

    for i in prices:
        price = i.text
        Prices.append(price)

    # print(Prices)

    descs = box.find_all("ul", class_ = "G4BRas")

    for i in descs:
        desc = i.text
        Description.append(desc)

    # print(Description)

    ratings = box.find_all("div", class_ = "XQDdHH")

    for i in ratings:
        rating = i.text
        Reviews.append(rating)

    # print(len(Reviews))

    images = box.find_all("img", class_= "DByuf4")

    for i in images:
        image = i["src"]
        Images.append(image)

    # print(Images)

data_frame = pd.DataFrame({"Product Name": Product_name, "Prices": Prices, "Description": Description, "Reviews": Reviews, "Images": Images})
# print(data_frame)

data_frame.to_csv("flipkart_mobile_under_15000.csv", index = False)

data_frame.to_json("flipkart_mobile_under_15000.json", orient="records", indent=2)
    
    
    
    # print(soup.prettify())
    # while True:
    # next_page = soup.find("a", class_ = "_9QVEpD").get("href")
    # complete_url = "https://www.flipkart.com" + next_page #get complete url
    # print(next_page)
    # print(complete_url)
    # url = complete_url
    # r = requests.get(url)
    # soup = BeautifulSoup(r.text, "lxml")

