import urllib.request
from inscriptis import get_text

url = "https://semesterspick.ch"
html = urllib.request.urlopen(url).read().decode('utf-8')

f = open("semesterspick.txt", "r")
text = get_text(f)
print(text)