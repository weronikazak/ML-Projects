from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

my_url = "https://www.newegg.com/p/pl?d=GTX&N=-1&IsNodeId=1&bop=And&Page=1&PageSize=36&order=BESTMATCH"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

f = open("file.csv", "w")
headers = "brand;product_name;shipping\n"
f.write(headers)

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", {"class":"item-container"})[:-4]
priceContainer = page_soup.findAll("li", {"class":"price-ship"})
i = 0

for container in containers:
    brand = container.a.img["title"]

    title_container = container.find_all("a", {"class":"item-title"})
    product_name = title_container[0].text.strip()

    shipping = priceContainer[i].text.strip()
    i += 1

    print("Brand: " + brand)
    print("Product name: ", product_name)
    print("Shipping: ", shipping)

    f.write(f"brand{brand};{product_name};{shipping}\n")

f.close()