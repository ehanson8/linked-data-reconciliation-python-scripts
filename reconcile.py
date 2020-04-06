import csv
import json
import requests
import xml.etree.ElementTree as ET

import click
from fuzzywuzzy import fuzz


@click.group()
def main():
    """"""
    pass


def compare(value1, value2):
    """"""
    ratio = fuzz.ratio(value1, value2)
    partialRatio = fuzz.partial_ratio(value1, value2)
    tokenSort = fuzz.token_sort_ratio(value1, value2)
    tokenSet = fuzz.token_set_ratio(value1, value2)
    match_pct = (ratio + partialRatio + tokenSort + tokenSet) / 4
    return match_pct


@main.command()
@click.option('-f', '--name_file', prompt='Enter name file',
              help='The file with the names to be searched.')
@click.option('-a', '--auth_file', prompt='Enter the file of authorities',
              help='The file with the names to be searched against.')
@click.option('-n', '--name_col', prompt='Enter the name column',
              help='The column containing the names to use for the search.')
@click.option('-u', '--auth_col', prompt='Enter the auth column',
              help='The column containing the names to search against.')
@click.option('-t', '--threshold', prompt='Enter the threshold',
              help='The threshold for the match percentage.')
def authfile(name_file, auth_file, name_col, auth_col, threshold):
    with open(f'{name_file}_auth_results.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(['match_pct'] + ['search_name'] + ['auth_name']
                        + ['comments'])
        auth_names = []
        with open(auth_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                auth_names.append(row[auth_col])
        with open(name_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for auth_name in auth_names:
                    match_pct = compare(row[name_col], auth_name)
                    if match_pct >= float(threshold):
                        writer.writerow([match_pct] + [row[name_col]]
                                        + [auth_name] + [''])


@main.command()
@click.option('-f', '--file_name', prompt='Enter file name',
              help='The file with the names to be searched.')
@click.option('-i', '--index_col', prompt='Enter the index column',
              help='The column containing the index to use for the search.')
@click.option('-n', '--name_col', prompt='Enter the name column',
              help='The column containing the names to use for the search.')
def viaf(file_name, index_col, name_col):
    NS = {'lc': 'http://www.loc.gov/zing/srw/'}
    with open(f'{file_name}_viaf_results.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(['search'] + ['result'] + ['viaf'] + ['match_pct']
                        + ['match'] + ['comments'])
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                viaf_uri = ''
                search_str = row[name_col].strip()
                index = row[index_col]
                params = {}
                query = f'local.{index} = "{search_str}"'
                params['query'] = query
                params['sortKeys'] = 'holdingscount'
                params['maximumRecords'] = '1'
                params['httpAccept'] = 'application/rdf+json'
                response = requests.get('http://viaf.org/viaf/search/viaf',
                                        params=params).content
                xml_resp = ET.fromstring(response)
                records = xml_resp.find('lc:records', namespaces=NS)
                if records is not None:
                    record = records.find('lc:record', namespaces=NS)
                    record = record.find('lc:recordData', namespaces=NS).text
                    json_rec = json.loads(record)
                    label = json_rec['mainHeadings']['data']
                    if isinstance(label, list):
                        viaf_label = label[0]['text']
                    else:
                        viaf_label = label['text']
                    viaf = json_rec['viafID']
                    match_pct = compare(search_str, viaf_label)
                    viaf_uri = f'http://viaf.org/viaf/{viaf}'
                    writer.writerow([search_str] + [viaf_label] + [viaf_uri]
                                    + [match_pct] + [''] + [''])
                else:
                    writer.writerow([search_str] + [''] + [''] + [''] + ['']
                                    + [''])


if __name__ == '__main__':
    main()
