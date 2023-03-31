from urllib.parse import urlsplit

import requests
import os
from dotenv import load_dotenv


def get_shorten_link(long_link, url, headers):
    payload = {
        'long_url': long_link
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def get_count_clicks(bitlink, headers):
    payload = {
        'unit': 'day',
        'units': '-1'
    }
    bitlink = urlsplit(bitlink)
    link_clicks = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc + bitlink.path}/clicks/summary'
    response = requests.get(link_clicks, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url_user, base_url, headers):
    url = urlsplit(url_user)
    base_url = base_url + url.netloc + url.path
    response = requests.get(base_url, headers=headers)
    if response.ok:
        return True
    else:
        return False


def main():
    load_dotenv()
    URL = "https://api-ssl.bitly.com/v4/bitlinks/"
    TOKEN = os.environ['BYTLY_TOKEN']
    HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    url = input('Enter url: ')
    if is_bitlink(url, URL, HEADERS):
        print(get_count_clicks(url, HEADERS))
    else:
        print('Bitlink', get_shorten_link(url, URL, HEADERS))


if __name__ == "__main__":
    main()
