from urllib.parse import urlsplit

import requests
import os
from dotenv import load_dotenv


def shorten_link(url, base_url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url
    }
    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def get_count_clicks(bitlink, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'unit': 'day',
        'units': '-1'
    }
    link_clicks_url = f'{bitlink}/clicks/summary'
    response = requests.get(link_clicks_url, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url_netloc_and_path, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url_netloc_and_path, headers=headers)
    return response.ok


def main():
    load_dotenv()
    base_url = "https://api-ssl.bitly.com/v4/bitlinks/"
    token = os.environ['BYTLY_TOKEN']

    url = input('Enter url: ')
    url_split = urlsplit(url)
    base_url_with_search_url = f'{base_url}{url_split.netloc}{url_split.path}'
    if is_bitlink(base_url_with_search_url, token):
        print(get_count_clicks(base_url_with_search_url, token))
    else:
        print('Bitlink', shorten_link(url, base_url, token))


if __name__ == "__main__":
    main()
