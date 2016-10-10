import requests
import csv
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import urllib

baseURL = 'http://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString='
typeQualifier = '&QueryClass=organisation'#Use DBpedia classes listed here (http://mappings.dbpedia.org/server/ontology/classes/) to refine results provided that all of the entities in the source file are of the same types
f=csv.writer(open('dbpediaResultsCorporate.csv', 'wb'))
f.writerow(['search']+['result']+['ratio']+['partialRatio']+['tokenSort']+['tokenSet']+['avg']+['uri'])
with open('organizations.txt') as txt:
    for row in txt:
        rowEdited = urllib.quote(row.decode('utf-8-sig').encode('utf-8').strip())
        url = baseURL+rowEdited.strip()+typeQualifier
        response = requests.get(url).content
        record = BeautifulSoup(response, "lxml").find('html').find('body').find('arrayofresult').find('result')
        try:
            label = record.find('label').text.encode('utf-8')
            uri = record.find('uri').text
        except:
            label = ''
            uri = ''
        ratio = fuzz.ratio(row, label)
        partialRatio = fuzz.partial_ratio(row, label)
        tokenSort = fuzz.token_sort_ratio(row, label)
        tokenSet = fuzz.token_set_ratio(row, label)
        avg = (ratio+partialRatio+tokenSort+tokenSet)/4
        f=csv.writer(open('dbpediaResultsCorporate.csv', 'a'))
        f.writerow([row.strip()]+[label]+[ratio]+[partialRatio]+[tokenSort]+[tokenSet]+[avg]+[uri])
