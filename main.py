import os
import argparse

from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def shorten_link(link, headers):
    url = "https://api-ssl.bitly.com/v4/shorten"
    payload = {"long_url": link}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(link, headers):
    clicks_count_link = (
        f"https://api-ssl.bitly.com/v4/bitlinks/"
        f"{link}/clicks/summary"
    )
    response = requests.get(clicks_count_link, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(user_link, headers):
    url = (
        f"https://api-ssl.bitly.com/v4/bitlinks/"
        f"{urlparse(user_link).netloc}{urlparse(user_link).path}"
    )
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    headers = {'Authorization': 'Bearer {}'.format(bitly_token)}
    parser = argparse.ArgumentParser(
        description='''Сокращает ссылку/
        проверяет кол-во переходов по сокращённой ссылке'''
    )
    parser.add_argument('--url', help='ссылка')
    args = parser.parse_args()

    try:
        if is_bitlink(args.url, headers):
            click_count = count_clicks(args.url, headers)
            print("Кол-во переходов по ней: ", click_count)

        else:
            bitly_link = shorten_link(args.url, headers)
            print("Сокращённая ссылка: ", bitly_link)

    except requests.exceptions.HTTPError as error:
        print("Can't get data from server:\n{0}".format(error))

if __name__ == "__main__":
    main()
