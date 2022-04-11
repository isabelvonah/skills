import csv
from datetime import datetime
from time import strftime
import time
import random
import requests
from inscriptis import get_text
from bs4 import BeautifulSoup


ids = []

with open("results/result_marketing-communications-editorial_online-marketing-social-media.csv", 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ids.append(row[0])

# forms the url
def get_url(id):
    template = "https://www.jobs.ch/en/vacancies/detail/{}/?source=vacancy_search"
    url = template.format(id)
    return url

# returns a tuple of job attributes
def get_offer(soup):

    title_div = soup.find("h1")
    title = title_div.get("title")

    spans = soup.find_all("span", "Span-sc-1ybanni-0")
    date = spans[14].get("title")
    position = spans[15].get("title")
    workload = spans[16].get("title")
    place = spans[10].get("title")

    cat_div = soup.find("div", "Div-sc-1cpunnt-0 ffMwOV")
    categories = cat_div.get_text()[10:]

    links = soup.find_all("a", "Link__ExtendedRRLink-sc-czsz28-1 Link-sc-czsz28-2 jEnTUT")
    company = links[0].get_text()
  
    offer_div = soup.find("div", "Div-sc-1cpunnt-0 DetailVacancyView__StyledVacancyDetailWrapper-sc-8f0fxs-0 jzJSph gpGrF")
    iframe = offer_div.div
    # uses inscriptis instead of Beautiful Soup
    text = get_text(str(iframe))

    # The date of the request is also required as a log attribute
    today = datetime.today(),strftime('%y-%m-%d')

    offer = (ids[i], title, date, company, place, position, workload, categories, text, today)
    return offer

# The csv-file for the results gets created and prepared with the title row
with open('results/03_scrape_offers.csv', 'w', newline='', encoding='utf-8') as f:
   writer = csv.writer(f)
   writer.writerow(['id', 'title', 'date', 'company', 'place', 'position', 'workload', 'categories', 'text', 'today'])

for i in range(len(ids)):

    url = get_url(ids[i])

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # to slow the algorithm down and don't send too many requests at once
    time.sleep(random.randint(0,5))

    try:
        offer = get_offer(soup)
    
        with open('results/03_scrape_offers.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(offer)

    except: pass


