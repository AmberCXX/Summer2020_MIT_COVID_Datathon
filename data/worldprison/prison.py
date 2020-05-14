import pandas as pd
import requests
import json
import string
from bs4 import BeautifulSoup
from collections import OrderedDict
from tqdm import tqdm


def parse(url):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'html.parser')
    basic_data = soup.find('div', {'id': 'basic_data'})
    data = OrderedDict()
    t = str.maketrans('', '', '\n\t\r')
    try:
        for row in basic_data.find_all('tr'):
            try:
                label = row.find('th').text.translate(t)
                if label.startswith('Prison population trend'):
                    content = []
                    table = row.find('table')
                    for subrow in table.find_all('tr')[1:]:
                        a = subrow.text.translate(t).split()
                        content.append({
                            'Year': a[0],
                            'Prison population total': a[1],
                            'Prison population rate': a[2]
                        })
                else:
                    content = row.find('td').text.translate(t)
                data[label] = content
            except AttributeError:
                continue
    except AttributeError:
        print('ERROR: ' + url)
    return data

def main():
    countries = pd.read_csv('countries.csv').to_numpy()
    base_url = 'https://www.prisonstudies.org/country/'
    data = {}
    for row in tqdm(countries):
        url = base_url + row[1]
        data[row[0]] = parse(url)

    with open('prison.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
