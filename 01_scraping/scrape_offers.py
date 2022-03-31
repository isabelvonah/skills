import csv
from datetime import datetime
from time import strftime
import time
import random
import requests
from inscriptis import get_text
from bs4 import BeautifulSoup


# These id's serve as examples. Eventually, a function should iterate over a list of id's and modify the url accordingly
ids = ["b28c5f6c-8af3-4325-927f-0a06a9105e75", "32289881-3fa2-47e2-b9c4-d66348aa099e", "a1513ed6-9763-4618-a866-1527f6dd17c6", "6a24f7ee-fd7a-4246-bf62-57b384d609a9"]

# forms the url
def get_url(id):
    template = "https://www.jobs.ch/en/vacancies/detail/{}/?source=vacancy_search"
    url = template.format(id)
    return url

# The csv-file for the results gets created and prepared with the title row
# must be commented out when adding additional rows instead of creating a new file
with open('offers.csv', 'w', newline='', encoding='utf-8') as f:
   writer = csv.writer(f)
   writer.writerow(['id', 'title', 'date', 'company', 'place', 'position', 'workload', 'categories', 'text'])

for i in range(len(ids)):

    url = get_url(ids[i])

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    title_div = soup.find("h1")
    title = title_div.get("title")

    spans = soup.find_all("span", "Span-sc-1ybanni-0")
    date = spans[14].get("title")
    position = spans[15].get("title")
    workload = spans[16].get("title")
    place = spans[10].get("title")

    links = soup.find_all("a", "Link__ExtendedRRLink-sc-czsz28-1 Link-sc-czsz28-2 jEnTUT")
    company = links[0].get_text()
    categories = ""
    for i in range(len(links)-2):
        categories += links[i+1].get_text()
        categories += ", "
    categories = categories[:-2]
  
    offer_div = soup.find("div", "Div-sc-1cpunnt-0 DetailVacancyView__StyledVacancyDetailWrapper-sc-8f0fxs-0 jzJSph gpGrF")
    iframe = offer_div.div
    text = get_text(str(iframe))

    offer = (ids[i], title, date, company, place, position, workload, categories, text)
    
    with open('offers.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(offer)


