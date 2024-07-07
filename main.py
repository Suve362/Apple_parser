import requests
from bs4 import BeautifulSoup
from pprint import pprint
import unicodedata
import re
from time import time
from typing import Any
from functools import wraps

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'}

pattern = re.compile(r'(^\d\s*,\s*)|(,*\s*:,)')

'''<main id="main" class="main" role="main" data-page-type="specs"> airpods 3'''


def time_count(func: Any):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f'Время работы: {end - start:.4f} c.')
        return result

    return wrapper


@time_count
def spec_function(name: str):
    url = f'https://www.apple.com/{name}/specs/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    main_name = soup.find('h1', class_='visuallyhidden').text
    all_spec = soup.find_all('main', id='main') if name == 'airpods-3rd-generation' else soup.find_all(
        'div', class_='techspecs-row')
    print(main_name.upper() + '\n')
    for i in all_spec:
        string_spec = i.stripped_strings
        string_specs = i.stripped_strings
        spec = ''.join([i for i in string_spec][0])
        print(f'{spec}')
        specs = pattern.sub(lambda match: "" if match.group(1) else ":", unicodedata.normalize('NFKC', ', '.join(
            [j for j in string_specs]).replace(spec, '').lstrip('(\', ')))
        pprint(specs, width=100, compact=True)
        print('-' * 100)


name_dict = {'mac': 'macbook air, macbook pro, imac, mac mini, mac studio, mac pro',
             'ipad': 'ipad pro, ipad air, ipad 10.9, ipad mini, apple pencil, ipad keyboards',
             'iphone': 'iphone 15 pro, iphone 15, iphone 14, iphone 13, iphone se',
             'apple watch': 'apple watch series 9, apple watch ultra 2, apple watch se',
             'vision pro': 'apple vision pro',
             'airpods': 'airpods 2nd generation, airpods 3rd generation, airpods pro, airpods max',
             'other': 'apple tv 4k, homepod 2nd generation, homepod mini, airtag'
             }


def main():
    while True:
        try:
            initial_string = input(f'Choose one from list: {', '.join(name_dict.keys())}\n').lower().strip(' ')
            if initial_string in name_dict.keys():
                print(name_dict[f'{initial_string}'])
                break
            else:
                print('Incorrect string, write it again\n')
        except KeyboardInterrupt:
            exit()

    while True:
        try:
            name_string = input()
            string = '-'.join(name_string.lower().split(' '))
            spec_function(string)
            break
        except AttributeError:
            print('Incorrect name, write it again:')
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    main()
