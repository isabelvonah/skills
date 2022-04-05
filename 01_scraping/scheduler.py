import schedule
import time
import csv

import scrape_meta as sm

with open('filters.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(', '.join(row))

def job():
    print("I'm working...")

