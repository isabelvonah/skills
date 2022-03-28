import csv
from datetime import datetime
from time import strftime
import time
import random
import requests
from bs4 import BeautifulSoup

cat = "information-technology-telecom"
subcat = "database-specialists-development"

def get_url(page):
    template = "https://www.jobs.ch/en/vacancies/{}/{}/?page={}term="
    url = template.format(cat, subcat, page)
    return url

def get_job(article, page, cat, subcat):
    atag = article.a

    id = str(atag.get('href'))[21:57]
    title = atag.get('title')
    promo = False
    if str(atag.get('href')).find('promo') != -1:
        promo = True
    today = datetime.today(),strftime('%y-%m-%d')
    
    job = (id, cat, subcat, page, title, promo, today)
    return job

url = get_url(0)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

navigation_span = soup.find("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 fJEZEL")
number_of_pages = int(str(navigation_span)[-11:-7].replace("/",""))

jobs = []

# for i in range(number_of_pages):
for i in range(3):
    
    page = i + 1
    url = get_url(i + 1)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('article')

    for article in articles:
        job = get_job(article, page, cat, subcat)
        jobs.append(job)
        #time.sleep(random.randint(0,9))
        #print("looped")

with open('urls_3.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'cat', 'subcat', 'page', 'title', 'promo', 'date'])
    writer.writerows(jobs)



