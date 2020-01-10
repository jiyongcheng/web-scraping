# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import xlwt
from datetime import datetime
import re

def saveToFile(string, file=None):
    if file==None:
        file = "output.txt"
    f= open(file,"w+")
    f.write(string)
    f.close()

def getInstagramLink(href):
    response = requests.get(href,timeout=2)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    aLinks = soup.find('a', href=lambda href: href and ("http://instagram.com" in href or "https://instagram.com" in href))
    
    print(aLinks)
    # for node in aLinks:
    #     if len(node['href']) > 0:
    #         return node['href']
    return ''
def getUrls(text):
    # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(text, "html.parser")
    td = soup.find_all('td', attrs={"data-title":'Store Address'})

    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')

    ws.write(0, 0, 'Website')
    ws.write(0, 1, 'Email')
    ws.write(0, 2, 'Instagram')

    for i in range(len(td)):
        node = td[i]
        children = node.findChildren('a', recursive = False)
        for child in children:
            print(child['href'])
            href = child['href']
            instagramLink = getInstagramLink(href)
            ws.write(i+1, 0, href)
            ws.write(i+1, 2, instagramLink)
            wb.save('example.xls')

baseUrl = 'https://www.shopistores.com/shopify/'
i = 1
url = baseUrl + str(i)
# Connect to the URL
response = requests.get(url)
if (response.text):
    getUrls(response.text)


# while True:
#     # Set the URL you want to webscrape from
#     url = baseUrl + str(i)
#     # Connect to the URL
#     response = requests.get(url)
#     if (response.text):
#         getUrls(response.text)
#         i = i + 1
#         print(url)
#     else:
#         break
# print(response.text)






