import requests
import csv
from bs4 import BeautifulSoup
import difflib
from fuzzywuzzy import fuzz
import urllib

baseURL = 'http://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString='
typeQualifier = '&QueryClass=person'#Use DBpedia classes listed here (http://mappings.dbpedia.org/server/ontology/classes/) to refine results provided that all of the entities in the source file are of the same types
f=csv.writer(open('dbpediaResultsPeople.csv', 'wb'))
f.writerow(['search']+['searchDirectOrder']+['result']+['seq']+['ratio']+['partialRatio']+['tokenSort']+['tokenSet']+['avg']+['uri'])
with open('people.txt') as txt:
    for row in txt:
        rowDirect = row.strip()[row.find(',')+2:]+' '+row[:row.find(',')]
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
        if row.find(',') != -1:
            seq = round(difflib.SequenceMatcher(None, rowDirect, label).ratio()*100, 0)
            ratio = fuzz.ratio(rowDirect, label)
            partialRatio = fuzz.partial_ratio(rowDirect, label)
            tokenSort = fuzz.token_sort_ratio(rowDirect, label)
            tokenSet = fuzz.token_set_ratio(rowDirect, label)
        else:
            seq = round(difflib.SequenceMatcher(None, row, label).ratio()*100, 0)
            ratio = fuzz.ratio(row, label)
            partialRatio = fuzz.partial_ratio(row, label)
            tokenSort = fuzz.token_sort_ratio(row, label)
            tokenSet = fuzz.token_set_ratio(row, label)
            rowDirect = 'N/A'
        avg = (seq+ratio+partialRatio+tokenSort+tokenSet)/5
        f=csv.writer(open('dbpediaResultsPeople.csv', 'a'))
        f.writerow([row.strip()]+[rowDirect]+[label]+[seq]+[ratio]+[partialRatio]+[tokenSort]+[tokenSet]+[avg]+[uri])
