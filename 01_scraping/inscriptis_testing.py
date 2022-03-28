import urllib.request
from inscriptis import get_text

url = "https://www.jobs.ch/en/vacancies/detail/37f5dcc7-2161-4f00-be57-eaa673c4751c/?source=vacancy_search"

html = urllib.request.urlopen(url).read().decode('utf-8')

text = get_text(html)

with open("test.txt", "w") as text_file:
    text_file.write(text)