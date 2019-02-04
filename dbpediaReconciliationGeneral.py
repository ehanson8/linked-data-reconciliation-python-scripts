import requests
import csv
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import urllib

baseURL = 'http://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString='


f=csv.writer(open('dbpediaResultsGeneral.csv', 'w'))
f.writerow(['search']+['result']+['description']+['ratio']+['partialRatio']+['tokenSort']+['tokenSet']+['avg']+['uri'])
with open('organizations.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = str(row['name'])
        nameEdited = urllib.parse.quote(name.strip())
        url = baseURL+nameEdited.strip()
        response = requests.get(url).content
        record = BeautifulSoup(response, "lxml").find('html').find('body').find('arrayofresult').find('result')
        try:
            label = record.find('label').text
            uri = record.find('uri').text
            description = record.find('description').text
        except:
            label = ''
            uri = ''
            description = ''
        ratio = fuzz.ratio(name, label)
        partialRatio = fuzz.partial_ratio(name, label)
        tokenSort = fuzz.token_sort_ratio(name, label)
        tokenSet = fuzz.token_set_ratio(name, label)
        avg = (ratio+partialRatio+tokenSort+tokenSet)/4
        f=csv.writer(open('dbpediaResultsGeneral.csv', 'a'))
        f.writerow([name.strip()]+[label]+[description.strip()]+[ratio]+[partialRatio]+[tokenSort]+[tokenSet]+[avg]+[uri])
