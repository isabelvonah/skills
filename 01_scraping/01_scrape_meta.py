import csv
from datetime import datetime
from time import strftime
import requests
from bs4 import BeautifulSoup
import time
import random


# forms the url
def get_url(cat, subcat, employment_typ, industry, page):

    template = "https://www.jobs.ch/en/vacancies/{}/{}/?employment-type={}&industry={}&page={}term="
    url = template.format(cat, subcat, employment_typ, industry, page)
    return url


# returns a tuple of job attributes
# article represents one result of a job search page
def get_job(article, page, cat, subcat, employment_typ, industry):

    # The a-tag links to a url including the unique id of the job offer and also delivers the title of the offer
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
    
    # The date of the request is also required as a log attribute
    today = datetime.today(),strftime('%y-%m-%d')

    # all attributes are stored in a tuple and returned
    job = (id, cat, subcat, employment_typ, industry, page, title, company, place, promo, today)
    return job


# scrapes through one query (with the same filters) and goes through multiple pages if necessary
def scrape(cat,subcat,employment_typ,industry):

    # The first page gets loaded to detect the number of pages
    url = get_url(cat, subcat, employment_typ, industry, 0)

    # to slow the algorithm down and don't send too many requests at once
    time.sleep(random.randint(0,5))

    # requests first result page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # detects the number of pages according to the navigation element of the first page
    navigation_span = soup.find_all("span", "Span-sc-1ybanni-0 Text__span-sc-1lu7urs-8 Text-sc-1lu7urs-9 fJEZEL")
    if len(navigation_span) == 0:
        number_of_pages = 1
    else:
        number_of_pages = int(str(navigation_span[0])[-11:-7].replace("/",""))

    # preparation of filename for result file
    file = "result_" + cat + "_" + subcat

    # for every page of the results gets analysed with BeautifulSoup and written (appended) into the created csv-file 
    for i in range(number_of_pages):
        
        jobs = []
        page = i + 1
        url = get_url(cat, subcat, employment_typ, industry, page)

        # to slow the algorithm down and don't send too many requests at once
        time.sleep(random.randint(0,5))

        # requests result page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        # finds all article-tags which represent one job offer
        articles = soup.find_all('article')

        # if there's no article-tag (len(articles) == 0), there's no result for this filter and the next steps are not needed / possible
        if len(articles) != 0:

            # goes through all articles (job offers)
            for article in articles:
                job = get_job(article, page, cat, subcat, employment_typ, industry)
                jobs.append(job)

            with open("01_scrape_meta/" + file + '.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(jobs)


# goes through all possible filters (employment typ, industry) for one category and subcategory
def scrape_cat(cat, subcat):

    # preparation of filename
    file = "result_" + cat + "_" + subcat

    # creation of the csv-file
    with open("01_scrape_meta/" + file + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'cat', 'subcat', 'employment-typ', 'industry', 'page', 'title', 'company', 'place', 'promo', 'date'])
    
    counter = 0

    # goes through all employment_typ's
    for et in range(6):
        # goes through all industries
        for ind in range(24):

            # prints message after every 10 requests
            counter += 1
            if counter%10 == 0:
                print(cat + " / " + subcat + ": " + str(counter) + " / " + str(6 * 24) + "    " + datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))

            scrape(cat, subcat, str(et + 1), str(ind + 1))
    
    # prints message after every subcategory
    print("finished: " + cat + " / " + subcat + "    " + datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))


categories = {
    "admin-hr-consulting-ceo": [
        "ceo-management",
        "secretary-reception",
        "management-assistance",
        "processing-language-translation",
        "hr-management-development",
        "personnel-placement-consultancy",
        "consultancy-company-development",
        "quality-management",
        "legal-attorneys-court",
        "regulatory-affairs"],
    "finance-trusts-real-estate": [
        "auditing-revision-auditing",
        "controlling",
        "finance"],
    "banking-insurance": [
        "asset-portfolio-management",
        "actuary-mathematics",
        "financial-business-analysis",
        "funds-stocks-trade",
        "risk-management-compliance",
        "treasury-controlling-auditing",
        "project-management"],
    "purchasing-logistics-trading": [
        "logistics-supply-chain"],
    "marketing-communications-editorial": [
        "online-marketing-social-media",
        "product-brand-management"],
    "information-technology-telecom": [
        "testing-audit-security",
        "consultancy-business-informatics",
        "database-specialists-development",
        "network-specialists-engineers",
        "project-management-analysis",
        "erp-sap-crm",
        "software-architecture-engineering",
        "software-development",
        "web-programming-mobile",
        "system-engineering",
        "system-administration"],
    "chemical-pharma-biotechnology": [
        "biology-biotechnology",
        "chemical-r-d-analysis-production",
        "pharmaceutical-r-d-analysis-production",
        "quality-assurance-management"],
    "electronics-engineering-watches": [
        "electronics-electrotechnics",
        "medical-equipment-engineering",
        "quality-assurance-management"],
    "machine-plant-engin-manufacturing": [
        "automation-process-engineering",
        "quality-assurance-management"],
    "public-admin-education-social": [
        "public-administration",
        "science-research",
        "teaching-lecturing"] 
}

# goes through all categories given
for cat in categories.keys():
    array = categories.get(cat)
    for subcat in array:
        scrape_cat(cat, subcat)


# note:
empl_typs = {
    "Temporary": 1,
    "Freelance": 2,
    "Internship": 3,
    "Supplementary income": 4,
    "Unlimited employment": 5,
    "Apprenticeship": 6
}
