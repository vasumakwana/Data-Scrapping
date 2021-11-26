#pip install requests
#pip install bs4
#pip install html5lib

import requests
from bs4 import BeautifulSoup
import csv


url = "https://www.supremenewyork.com/shop"

r = requests.get(url)
hc = r.content

soup = BeautifulSoup(hc, 'html.parser')

mainclass = soup.find("div", {"id": "shop-scroller-container"})
liclass = mainclass.find_all("a")

all_links = set()

for link in liclass:
    l = link.get('href')
    all_links.add("https://www.supremenewyork.com" +l)

all_links = list(all_links)
filename = "info.csv"
f = open(filename,"w")
headers = "Title,Product URL,Price,Colors,Sizes,Image URLs,Add to Cart\n"
f.write(headers)

for innerurl in all_links:
    r1 = requests.get(innerurl)
    hc1 = r1.content
    soup1 = BeautifulSoup(hc1, 'html.parser')

    #title
    mc1 = soup1.find("div", {"id": "details"})
    h1tags = mc1.find("h1")
    title = h1tags.text.strip()

    #producturl
    producturl = innerurl

    #price
    ptags = mc1.find("p", {"class": "price"})
    price = ptags.text.strip()

    #Image Links
    ultags = mc1.find("ul", {"class": "styles"})
    litags = ultags.find("li")
    alinks = []
    for tag in ultags.find_all('a'):
        l1 = tag.get('href')
        alinks.append("https://www.supremenewyork.com" + l1)

    astrlinks = list(alinks)
    astr = ','.join([str(elem) for elem in alinks])

    #colors
    color = set()
    for innerurl in astrlinks:
        x1 = requests.get(innerurl)
        y1 = x1.content
        z1 = BeautifulSoup(y1, 'html.parser')
        x2 = z1.find("div", {"id": "details"})
        y2 = x2.find("p", {"class": "style"})
        color.add(y2.text)
        colorlist = list(color)
        colorstr = ','.join([str(elem) for elem in colorlist])


    print(title + "," + producturl + "," + price.replace(',', '') + "," "\""+colorstr+"\"" + "," "\""+astr+"\"" "\n")
    f.write(title + "," + producturl + "," + price.replace(',', '') + "," "\""+colorstr+"\"" + "," "\""+astr+"\"" "\n")


f.close()




