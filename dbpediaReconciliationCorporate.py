import requests
import csv
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import urllib

baseURL = 'http://lookup.dbpedia.org/api/search/KeywordSearch'
baseURL = baseURL + '?MaxHits=1&QueryString='
typeQualifier = '&QueryClass=organisation'  # Use DBpedia classes listed here
# (http://mappings.dbpedia.org/server/ontology/classes/) to refine results
# provided that all of the entities in the source file are of the same types
f = csv.writer(open('dbpediaResultsCorporate.csv', 'w'))
f.writerow(['search'] + ['result'] + ['ratio'] + ['partialRatio']
           + ['tokenSort'] + ['tokenSet'] + ['avg'] + ['uri'])
with open('organizations.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = str(row['name'])
        nameEdited = urllib.parse.quote(name.strip())
        url = baseURL + nameEdited.strip() + typeQualifier
        response = requests.get(url).content
        record = BeautifulSoup(response, "lxml").find('html').find('body')
        record = record.find('arrayofresult').find('result')
        try:
            label = record.find('label').text
            uri = record.find('uri').text
        except ValueError:
            label = ''
            uri = ''
        ratio = fuzz.ratio(name, label)
        partialRatio = fuzz.partial_ratio(name, label)
        tokenSort = fuzz.token_sort_ratio(name, label)
        tokenSet = fuzz.token_set_ratio(name, label)
        avg = (ratio + partialRatio + tokenSort + tokenSet) / 4
        f = csv.writer(open('dbpediaResultsCorporate.csv', 'a'))
        f.writerow([name.strip()] + [label] + [ratio] + [partialRatio]
                   + [tokenSort] + [tokenSet] + [avg] + [uri])
