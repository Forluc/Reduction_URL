from urllib.parse import urlsplit

import requests
import os
from dotenv import load_dotenv


def shorten_link(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url
    }
    base_url = "https://api-ssl.bitly.com/v4/bitlinks/"
    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def get_count_clicks(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'unit': 'day',
        'units': '-1'
    }
    base_url = "https://api-ssl.bitly.com/v4/bitlinks/"
    split_url = urlsplit(url)
    bitlink = f'{base_url}{split_url.netloc}{split_url.path}/clicks/summary'
    response = requests.get(bitlink, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    base_url = "https://api-ssl.bitly.com/v4/bitlinks/"
    split_url = urlsplit(url)
    bitlink = f'{base_url}{split_url.netloc}{split_url.path}'
    response = requests.get(bitlink, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BYTLY_TOKEN']

    url = input('Enter url: ')
    if is_bitlink(url, token):
        print(get_count_clicks(url, token))
    else:
        print('Bitlink', shorten_link(url, token))


if __name__ == "__main__":
    main()
