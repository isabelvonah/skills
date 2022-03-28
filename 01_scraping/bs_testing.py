import csv
from datetime import datetime
from time import strftime
import time
import random
from jinja2 import Undefined
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
    spans = article.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 cAoBYw eubypz")

    id = str(atag.get('href'))[21:57]
    title = atag.get('title')
    company = spans[0].get_text()
    try:
        place = spans[1].get_text()
    except:
        place = ""
    promo = False
    if str(atag.get('href')).find('promo') != -1:
        promo = True
    today = datetime.today(),strftime('%y-%m-%d')

    job = (id, cat, subcat, page, title, company, place, promo, today)
    return job

url = get_url(0)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

navigation_span = soup.find("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 fJEZEL")
number_of_pages = int(str(navigation_span)[-11:-7].replace("/",""))

#with open('urls_4.csv', 'w', newline='', encoding='utf-8') as f:
   # writer = csv.writer(f)
   # writer.writerow(['id', 'cat', 'subcat', 'page', 'title', 'company', 'place', 'promo', 'date'])

# for i in range(number_of_pages):
for i in range(number_of_pages):
    
    jobs = []

    page = i + 4
    url = get_url(i + 1)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('article')

    for article in articles:
        job = get_job(article, page, cat, subcat)
        jobs.append(job)
        #time.sleep(random.randint(0,9))
        #print("looped")

    with open('urls_4.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(jobs)



