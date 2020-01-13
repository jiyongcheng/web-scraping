# Import libraries
import requests
from requests.exceptions import Timeout
import urllib.request
import time
from bs4 import BeautifulSoup
import xlwt
from datetime import datetime
import re

REQUEST_TIMEOUT = 3
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
EMAIL_REG = '([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})'

def saveToFile(string, file=None):
    if file==None:
        file = "output.txt"
    f= open(file,"w+")
    f.write(string)
    f.close()

def requestUrl(url):
    return requests.get(url,timeout= REQUEST_TIMEOUT, headers=HEADERS)

def getEmailFromAboutUs(href):
    try:
        response = requestUrl(href)
    except Timeout:
        print('The reqeust timed out')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        aboutUsUri = soup.find('a', string= ["About Us"])
        if aboutUsUri is not None:
            # if the uri starts with /
            if aboutUsUri['href'].startswith('/'):
                url = href + aboutUsUri['href']
            else:
                url = aboutUsUri['href']
            print('about us url:' + url)
            try:
                response = requestUrl(url)
            except Timeout:
                print('The reqeust timed out')
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                email = soup.find(string=re.compile(EMAIL_REG + '$'))
                print(email)
                if email is not None:
                    print('email from about us------>' + email)
                    return email
                else:
                    email = soup.find(string=re.compile(EMAIL_REG + '$'))
                    if email is not None:
                        print('email from about us 2------>' + email.strip())
                        return email.strip()
                    else:
                        email = soup.find(string=re.compile(EMAIL_REG))
                        if email is not None:
                            print('email from about us 3------>' + email.strip())
                            return email.strip()
                        else:
                            return ''

    return ''

def getEmailFromContactUs(href):
    try:
        response = requestUrl(href)
    except Timeout:
        print('The reqeust timed out')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        contactUri = soup.find('a', string= ["Contact Us", "联系我们"])
        if contactUri is not None:
            # if the uri starts with /
            if contactUri['href'].startswith('/'):
                url = href + contactUri['href']
            else:
                url = contactUri['href']
            print('contact url:' + url)
            try:
                response = requestUrl(url)
            except Timeout:
                print('The reqeust timed out')
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                email = soup.find(string=re.compile(EMAIL_REG + '$'))
                print(email)
                if email is not None:
                    print('email from Contact us------>' + email)
                    return email
                else:
                    email = soup.find(string=re.compile(EMAIL_REG + '$'))
                    if email is not None:
                        print('email from Contact us 2------>' + email.strip())
                        return email.strip()
                    else:
                        email = soup.find(string=re.compile(EMAIL_REG))
                        if email is not None:
                            print('email from Contact us 3------>' + email.strip())
                            return email.strip()
                        else:
                            return ''

    return ''


def getEmailAddress(href):
    email = getEmailFromFacebook(href)
    if email is None or len(email) < 1:
        email = getEmailFromContactUs(href)
        if email is None or len(email) < 1:
            email = getEmailFromAboutUs(href)
    return email

def getEmailFromFacebook(href):
    try:
        response = requestUrl(href)
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
                try:
                    response = requestUrl(aboutLink)
                except Timeout:
                    print('The reqeust timed out- fetch email')
                else:
                    soup = BeautifulSoup(response.text, "html.parser")
                    emailLink = soup.find('a', href=lambda href: href and ('@' in href))
                    if emailLink is not None:
                        email = emailLink.text
                        print('email from FB:' + email)
                        return email

    return ''
def getInstagramLink(href):
    try:
        response = requestUrl(href)
    except Timeout:
        print('The reqeust timed out')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        aLink = soup.find('a', href=lambda href: href and ("instagram.com" in href))
        if aLink is None:
            return ''
        else:
            if len(aLink['href']) > 0:
                print('instagram:' + aLink['href'])
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
            print('******************************************'+ str(i))
            print('URL:' + child['href'])
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



# getEmailAddress('https://www.beeinspiredclothing.com/')






