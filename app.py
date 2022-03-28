import json
import requests
from serpapi import GoogleSearch



url = "https://indeed-indeed.p.rapidapi.com/apigetjobs"

querystring = {"format":"json","v":"2","jobkeys":"switzerland, schweiz","publisher":"undefined"}

headers = {
	"X-RapidAPI-Host": "indeed-indeed.p.rapidapi.com",
	"X-RapidAPI-Key": "3723442cffmsh8d1eb24173d8b54p1186aajsn184964ea6b04"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

with open('json_data_api.json', 'w') as outfile:
    json.dump(response, outfile)