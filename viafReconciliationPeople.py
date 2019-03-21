# -*- coding: utf-8 -*-
import requests
import csv
from fuzzywuzzy import fuzz
import json
import urllib
import html

baseURL = 'http://viaf.org/viaf/search/viaf?query=local.personalNames+%3D+%22'
f = csv.writer(open('viafPeopleResults.csv', 'w'))
f.writerow(['search'] + ['result'] + ['viaf'] + ['lc'] + ['isni'] + ['ratio']
           + ['partialRatio'] + ['tokenSort'] + ['tokenSet'] + ['avg'])
with open('people.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = str(row['name'])
        rowEdited = urllib.parse.quote(name.strip())
        urlSuffix = '%22+and+local.sources+%3D+%22lc%22&sortKeys=holdingscount'
        urlSuffix2 = '&maximumRecords=1&httpAccept=application/rdf+json'
        url = baseURL + rowEdited + urlSuffix + urlSuffix2
        print(url)
        response = requests.get(url).content.decode('utf-8')
        try:
            startString = '<recordData xsi:type="ns1:stringOrXmlFragment">'
            startIndex = response.index(startString)
            endString = '</recordData>'
            endIndex = response.index(endString)
            print(endIndex, startIndex)
            response = response[startIndex + 47: endIndex]
            response = response.replace('&quot;', '"')
            response = json.loads(response)
            label = response['mainHeadings']['data']
            if isinstance(label, list):
                label = label[0]['text']
            else:
                label = label['text']
            label = html.unescape(label)
            print(label)
            viafid = response['viafID']
        except ValueError:
            label = ''
            viafid = ''
        ratio = fuzz.ratio(name, label)
        partialRatio = fuzz.partial_ratio(name, label)
        tokenSort = fuzz.token_sort_ratio(name, label)
        tokenSet = fuzz.token_set_ratio(name, label)
        avg = (ratio + partialRatio + tokenSort + tokenSet) / 4

        if viafid != '':
            links = json.loads(requests.get('http://viaf.org/viaf/' + viafid
                               + '/justlinks.json').text)
            viafid = 'http://viaf.org/viaf/' + viafid
            try:
                lc = 'http://id.loc.gov/authorities/names/'
                lc = lc + json.dumps(links['LC'][0]).replace('"', '')
            except ValueError:
                lc = ''
            try:
                isni = 'http://isni.org/isni/'
                isni = isni + json.dumps(links['ISNI'][0]).replace('"', '')
            except ValueError:
                isni = ''
        else:
            lc = ''
            isni = ''
        f.writerow([name.strip()] + [label] + [viafid] + [lc] + [isni]
                   + [ratio] + [partialRatio] + [tokenSort]
                   + [tokenSet] + [avg])
