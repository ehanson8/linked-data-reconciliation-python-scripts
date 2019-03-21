import requests
import csv
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import urllib

baseURL = 'http://lookup.dbpedia.org/api/search/KeywordSearch'
baseURL = baseURL + '?MaxHits=1&QueryString='
typeQualifier = '&QueryClass=person'  # Use DBpedia classes listed here
# (http://mappings.dbpedia.org/server/ontology/classes/) to refine results
# provided that all of the entities in the source file are of the same types

f = csv.writer(open('dbpediaResultsPeople.csv', 'w'))
f.writerow(['search'] + ['searchDirectOrder'] + ['result'] + ['ratio']
           + ['partialRatio'] + ['tokenSort'] + ['tokenSet'] + ['avg']
           + ['uri'])
with open('people.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = str(row['name'])
        nameDirect = name.strip()[name.find(',') + 2:]
        nameDirect = nameDirect + ' ' + name[:name.find(',')]
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
        if name.find(',') != -1:
            ratio = fuzz.ratio(nameDirect, label)
            partialRatio = fuzz.partial_ratio(nameDirect, label)
            tokenSort = fuzz.token_sort_ratio(nameDirect, label)
            tokenSet = fuzz.token_set_ratio(nameDirect, label)
        else:
            ratio = fuzz.ratio(name, label)
            partialRatio = fuzz.partial_ratio(name, label)
            tokenSort = fuzz.token_sort_ratio(name, label)
            tokenSet = fuzz.token_set_ratio(name, label)
            nameDirect = 'N/A'
        avg = (ratio + partialRatio + tokenSort + tokenSet) / 4
        f = csv.writer(open('dbpediaResultsPeople.csv', 'a'))
        f.writerow([name.strip()] + [nameDirect] + [label] + [ratio]
                   + [partialRatio] + [tokenSort] + [tokenSet] + [avg] + [uri])
