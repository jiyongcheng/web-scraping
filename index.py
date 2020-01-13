# Import libraries
import requests
from requests.exceptions import Timeout
import urllib.request
import time
from bs4 import BeautifulSoup
import xlwt
from datetime import datetime
import re

REQUEST_TIMEOUT = 2

def saveToFile(string, file=None):
    if file==None:
        file = "output.txt"
    f= open(file,"w+")
    f.write(string)
    f.close()

def getEmailFromContactUs(href):
    try:
        response = requests.get(href,timeout= REQUEST_TIMEOUT)
    except Timeout:
        print('The reqeust timed out')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        contactUri = soup.find('a', string= ["Contact Us", "About Us"])
        print(contactUri)
        if contactUri is not None:
            # if the uri starts with /
            if contactUri['href'].startswith('/'):
                url = href + contactUri['href']
            else:
                url = contactUri['href']
            print('url:' + url)
            try:
                response = requests.get(url,timeout= REQUEST_TIMEOUT)
            except Timeout:
                print('The reqeust timed out')
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                email = soup.find(string=re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'))
                if email is not None:
                    print('email------>' + email)
                    return email
    return ''


def getEmailAddress(href):
    email = getEmailFromFacebook(href)
    if email is None or len(email) < 1:
        email = getEmailFromContactUs(href)
    return email

def getEmailFromFacebook(href):
    try:
        response = requests.get(href,timeout= REQUEST_TIMEOUT)
    except Timeout:
        print('The reqeust timed out')
    else:
        soup = BeautifulSoup(response.text, "html.parser")

        aLink = soup.find('a', href=lambda href: href and ('facebook.com' in href))
        if aLink is None:
            return ''
        else:
            if len(aLink['href']) > 0:
                if (aLink['href'].endswith('/')):
                    aboutLink = aLink['href'] + 'about'
                else:
                    aboutLink = aLink['href'] + '/about'
                print(aboutLink)
                try:
                    response = requests.get(aboutLink,timeout= REQUEST_TIMEOUT)
                except Timeout:
                    print('The reqeust timed out- fetch email')
                else:
                    soup = BeautifulSoup(response.text, "html.parser")
                    emailLink = soup.find('a', href=lambda href: href and ('@' in href))
                    if emailLink is not None:
                        email = emailLink.text
                        print(email)
                        return email

    return ''
def getInstagramLink(href):
    try:
        response = requests.get(href,timeout= REQUEST_TIMEOUT)
    except Timeout:
        print('The reqeust timed out')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        aLink = soup.find('a', href=lambda href: href and ("http://instagram.com" in href or "https://instagram.com" in href))
        if aLink is None:
            return ''
        else:
            if len(aLink['href']) > 0:
                return aLink['href']

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
            facebookLink = getEmailAddress(href)
            ws.write(i+1, 0, href)
            ws.write(i+1, 1, facebookLink)
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






