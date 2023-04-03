from urllib.parse import urlsplit

import requests
import os
from dotenv import load_dotenv

load_dotenv()
URL = "https://api-ssl.bitly.com/v4/bitlinks/"
TOKEN = os.environ['BYTLY_TOKEN']
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}


def get_shorten_link(long_link, url=URL, headers=HEADERS):
    payload = {
        'long_url': long_link
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def get_count_clicks(bitlink, headers=HEADERS):
    payload = {
        'unit': 'day',
        'units': '-1'
    }
    url_bitlink_clicks = f'{bitlink}/clicks/summary'
    response = requests.get(url_bitlink_clicks, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url_netloc_and_path, headers=HEADERS):
    response = requests.get(url_netloc_and_path, headers=headers)
    return response.ok


def main(base_url=URL):
    url = input('Enter url: ')
    url_split = urlsplit(url)
    url_netloc_and_path = f'{base_url}{url_split.netloc}{url_split.path}'
    if is_bitlink(url_netloc_and_path):
        print(get_count_clicks(url_netloc_and_path))
    else:
        print('Bitlink', get_shorten_link(url))


if __name__ == "__main__":
    main(URL)
