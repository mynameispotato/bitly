import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


TEMPLATE_API_LINK = "https://api-ssl.bitly.com/v4/bitlinks"


def shorter_link(link, headers):
    short_link = "https://api-ssl.bitly.com/v4/shorten"
    payload = {"long_url": link}
    response = requests.post(short_link, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(link, headers):
    clicks_count_link = f"{TEMPLATE_API_LINK}/{link}/clicks/summary"
    response = requests.get(clicks_count_link, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url, headers):
    parse_link = urlparse(url)
    link_bitly = f"{TEMPLATE_API_LINK}/{parse_link.netloc}{parse_link.path}"
    response = requests.get(link_bitly, headers=headers)

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
            bitly_link = shorter_link(args.url, headers)
            print("Сокращённая ссылка: ", bitly_link)

    except requests.exceptions.HTTPError as error:
        print("Can't get data from server:\n{0}".format(error))

if __name__ == "__main__":
    main()
