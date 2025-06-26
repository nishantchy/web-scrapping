import requests
from bs4 import BeautifulSoup #beautifulsoup is used for get requests

web = requests.get("https://www.tutorialsfreak.com/")

# print(web)

# print(web.status_code)

# print(web.content)

# print(web.url)

soup = BeautifulSoup(web.content, 'html.parser') #to make code strutured

# print(soup.prettify()) #beautify format

print(soup.title) #get title
print(soup.p) #get paragraph

print(soup.h1)

images = soup.find_all('img')

for i in images:
    print(i['src']) 