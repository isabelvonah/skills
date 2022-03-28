import urllib.request
from inscriptis import get_text

url = "https://www.fhgr.ch"
html = urllib.request.urlopen(url).read().decode('utf-8')

text = get_text(html)
print(text)