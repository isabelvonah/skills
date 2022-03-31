import csv
from datetime import datetime
from time import strftime
import time
import random
import requests
from bs4 import BeautifulSoup

# These categories serve as examples. Eventually, a function should iterate over a list of categories and modify the url accordingly
cat = "information-technology-telecom"
subcat = "database-specialists-development"
employment_typ = "5"
industry = "4"

# forms the url
def get_url(page):
    template = "https://www.jobs.ch/en/vacancies/{}/{}/??employment-type={}&industry={}&page={}term="
    url = template.format(cat, subcat, employment_typ, industry, page)
    return url

# returns a tuple of job attributes
# article represents one result of a job search page
def get_job(article, page, cat, subcat, employment_typ, industry):

    # The a-tag links to a url including the unique id of the job offer and also deliver the title of the offer
    # promotioned offers contain "promo"
    atag = article.a
    id = str(atag.get('href'))[21:57]
    title = atag.get('title')
    promo = False
    if str(atag.get('href')).find('promo') != -1:
        promo = True

    # The company and the place are stored in a span-tag with a special class
    # there are missing places
    spans = article.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 cAoBYw eubypz")    
    company = spans[0].get_text()
    try:
        place = spans[1].get_text()
    except:
        place = ""
    
    # The date of the request is also required
    today = datetime.today(),strftime('%y-%m-%d')

    # all attributes are stored in a tuple
    job = (id, cat, subcat, employment_typ, industry, page, title, company, place, promo, today)
    return job

# The first page gets loaded to detect the number of pages
url = get_url(0)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

navigation_span = soup.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 fJEZEL")
if len(navigation_span) == 0:
    number_of_pages = 1
else:
    number_of_pages = int(str(navigation_span[0])[-11:-7].replace("/",""))

# The csv-file for the results gets created and prepared with the title row
# must be commented out when adding additional rows instead of creating a new file
with open('urls_5.csv', 'w', newline='', encoding='utf-8') as f:
   writer = csv.writer(f)
   writer.writerow(['id', 'cat', 'subcat', 'employment-typ', 'industry', 'page', 'title', 'company', 'place', 'promo', 'date'])

# for every page of the results gets analysed with BeautifulSoup and written (appended) into the created csv-file 
for i in range(number_of_pages):
    
    jobs = []
    page = i + 1
    url = get_url(page)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('article')

    # goes through all articles (job offers)
    for article in articles:
        job = get_job(article, page, cat, subcat, employment_typ, industry)
        jobs.append(job)
        #time.sleep(random.randint(0,9))
        #print("looped")

    with open('urls_5.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(jobs)



