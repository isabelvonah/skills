import csv
from datetime import datetime
from time import strftime
import time
import random
import requests
import urllib3
from inscriptis import get_text
from bs4 import BeautifulSoup


ids = []

with open("02_eliminate_duplicates.csv", 'r', newline='', encoding='utf-8') as f:
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

    spans = soup.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 kKewXR")
    
    date = spans[0].span.get_text()
    position = spans[1].get_text().split(",")[0]
    workload = spans[1].get_text().split(", ")[1]

    place = soup.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 ddkvol")[0].contents[1].get_text()[2:]
    company = soup.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 ddkvol")[0].contents[0].get_text()
    
    cat_div = soup.find("div", "Div-sc-1cpunnt-0 ffMwOV")
    categories = cat_div.get_text()[10:]
    
    if soup.find("iframe"):

        iframe = soup.find("div", "Div-sc-1cpunnt-0 DetailVacancyView__StyledVacancyDetailWrapper-sc-8f0fxs-0 jzJSph gpGrF").iframe
        text = get_text(str(iframe.get("srcdoc")))

        # When the content of the offer isn't found, another request must be made
        if "Redirection failed" in text:
            iframe_temp = str(iframe.get("srcdoc"))
            new_link = BeautifulSoup(iframe_temp, "lxml").find("a").get("href")
            new_response = requests.get(new_link)
            new_soup = BeautifulSoup(new_response.text, 'lxml')
            text = get_text(str(new_soup.body))

    else:

        iframe = soup.find("div", "Div-sc-1cpunnt-0 DetailVacancyView__StyledVacancyDetailWrapper-sc-8f0fxs-0 jzJSph gpGrF")
        # uses inscriptis instead of Beautiful Soup
        text = get_text(str(iframe))

    # The date of the request is also required as a log attribute
    today = datetime.today(),strftime('%y-%m-%d')

    offer = (ids[i], title, date, company, place, position, workload, categories, text, today)
    return offer

# The csv-file for the results gets created and prepared with the title row
# with open('03_scrape_offers.csv', 'w', newline='', encoding='utf-8') as f:
#    writer = csv.writer(f)
#    writer.writerow(['id', 'title', 'date', 'company', 'place', 'position', 'workload', 'categories', 'text', 'today'])

# for receiving a control message while scraping
counter = 0

for i in range(len(ids)):

    # prints message after every 10 requests
    counter += 1
    if counter%10 == 0:
        print(str(counter) + " / " + str(len(ids)) + "    " + datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))

    url = get_url(ids[i])

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # to slow the algorithm down and don't send too many requests at once
    time.sleep(random.randint(0,2))

    try:
        offer = get_offer(soup)
    
        with open('03_scrape_offers_4.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(offer)

    except: pass


