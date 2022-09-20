import configparser
import argparse
import time

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='Running the application.'
)

parser.add_argument('-l', '--log', dest='log', type=str, default="",
                    help='The log write to file\npython main.py --log out.log')
parser.add_argument('-d', '--debug', dest='debug', action="store_true", default=False,
                    help='Debug mode\n-d or --debug')
parser.add_argument('-cc', '--cache', dest='cache', action="store_true", default=False,
                    help='Use requests cache\n-cc or --cache')

parser.add_argument('--random-page', dest='random', action="store_true", default=False,
                    help='Extract a random page\npython main.py --random-range')

args = parser.parse_args()
# config = configparser.ConfigParser()
# include config.file
# config.read("config.ini")

import requests as _requests
# Кешируем запросы
CACHE = args.cache
if CACHE:
    import requests_cache
    requests_cache.install_cache('requests_cache')
from tool import log
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Any, List, Union
import os
import csv
from itertools import count
from datetime import datetime
import random


if args.log:
    logger = log(__name__, args.log)
else:
    logger = log(__name__)


BASE_URL = "https://www.bazaraki.com"
proxies = {
    'http': 'http://127.0.0.1:8081',
    'https': 'http://127.0.0.1:8081'
}
cert = '/home/maxwellviksna/.mitmproxy/mitmproxy-ca-cert.pem'
DEBUG = args.debug
REPORT_PATH = os.path.join(os.getcwd(), datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + ".csv")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "scrubber-name": "bazaraki"
}
WAIT = 20

RANGE = range(1, 1)

if args.random:
    RANGE = random.sample(range(1, 1), 1)


@dataclass
class IData:
    name: str
    value: Any


class BaseParserException(Exception):
    """Базовое исключение"""
    pass


class NotUrlsException(BaseParserException):
    """Если нет каких то ссылок"""
    pass


class BadStatusCode(BaseParserException):
    """Сервер вернул плохой ответ"""
    pass


class ConnectionError(BaseParserException):
    """Проблемы с соединением"""
    pass


class Requests:
    """Класс обертка над библиотекой requests"""

    class Response:
        """Регистрация """
        def __init__(self, url, status_code):
            self.url = url
            self.status_code = status_code
            self.type_url = None

    _response_list: List[Response] = []
    COUNT = 0

    def get(self, *args, **kwargs):
        """get запрос"""
        Requests.COUNT += 1
        url = args[0]
        try:
            print(args)
            print(kwargs.items())

            res = _requests.get(*args, **kwargs)
            Requests._response_list.append(self.Response(url, res.status_code))
            if res.status_code == 200:
                logger.info(f"Response [{res.status_code}] {url}")
            else:
                logger.warning(f"Status code: {res.status_code} {url}")
                raise BadStatusCode(f"Bad status code: {res.status_code}")
        except _requests.exceptions.ConnectionError:
            Requests._response_list.append(self.Response(url, 900))
            logger.warning(f"Connection Error {url}")
            raise ConnectionError(f"Problem with {url} ")

        return res

    def post(self, *args, **kwargs):
        """post запрос"""
        pass

    def __del__(self):
        logger.info(self.requests_report())

    def requests_report(self):
        """Вывод статистики по парсингу"""
        status200 = list(filter(lambda x: x.status_code == 200, self._response_list))
        statusBad = list(filter(lambda x: x.status_code != 200, self._response_list))
        string = f"\n{'-'*14} requests result {'-'*14}\n" \
                 f"Urls {Requests.COUNT}\n" \
                 f"Good {len(status200)}\n" \
                 f"Bad  {len(statusBad)}\n" \
                 f"{'-'*45}"
        return string


requests = Requests()


class Product:
    """Объект парсинга"""
    bad_urls = []
    finally_data = list()
    links = []
    COLUMN_NAME = [
        "Id",
        "Posted",
        "Title",
        "Price",
        "Owner",
        "Description",
        "Views",
        "Url"
    ]

    def __init__(self, url):
        self.data = dict()
        response = requests.get(url, headers=HEADERS, proxies=proxies, verify=cert)
        # response = requests.get(url, headers=HEADERS)
        print(response)
        print(dir(response))
        soup = Product.get_soup(response.text)
        pid = soup.select_one(".number-announcement")
        posted = soup.select_one(".date-meta")
        address = soup.select_one("span[itemprop=address]")
        price = soup.select_one("div.announcement-price__cost")
        [x.extract() for x in price.select("div, b, meta")]

        author = soup.select_one("div.author-name")
        views = soup.select_one("span.counter-views")
        description = soup.select_one("div.announcement-description")

        self.data["Id"] = self.str_split(pid)
        self.data["Posted"] = self.str_split(posted)
        self.data["Address"] = self.str(address)
        self.data["Author"] = self.str(author)
        self.data["Views"] = self.str_split(views)
        self.data["Description"] = self.str(description)
        self.data["Url"] = url


        characteristics = soup.select("div.announcement-characteristics ul.chars-column li")
        char_dict = dict()
        for char in characteristics:
            key = char.select_one(".key-chars")
            value = char.select_one(".value-chars")
            char_dict[self.str(key).replace(":", "")] = self.str(value)
        self.data.update(char_dict)

        Product.finally_data.append(self.data)

    def dump_csv(self):
        pass

    def str(self, item: BeautifulSoup):
        string = item.text.strip()
        return string

    def str_split(self, item: BeautifulSoup):
        string = self.str(item)
        return string.split(": ")[1]

    @staticmethod
    def get_soup(html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        return soup

class Report:
    """
        self.rows => all data. rows [{data}, {data}]
    """
    def __init__(self, data):
        self.rows = data
        self.keys = self.get_keys()
        self.dump_csv()

    def dump_csv(self):
        with open(REPORT_PATH, 'w', newline='') as csvfile:
            fieldnames = self.keys
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)

        logger.info("Data write success to file *csv.")

    def get_keys(self):
        keys = list()

        for row in self.rows:
            for key in row.keys():
                if key not in keys:
                    keys.append(key)

        return list(keys)



class FunctionUnit:
    """Функциональный блок"""
    SHARE_DATA:Union[IData, Any] = None

    def __init__(self, func):
        self.func = func

    def run(self):
        self.func(FunctionUnit)

    def __call__(self, *args, **kwargs):
        self.func(FunctionUnit)


def search_content(cls: FunctionUnit):

    for x in RANGE:
        url = BASE_URL +f"/real-estate/houses-and-villas-sale/?page={x}"
        try:
            response = requests.get(url, headers=HEADERS, proxies=proxies, verify=cert)
            #response = requests.get(url, headers=HEADERS)
            soup = Product.get_soup(response.text)
            number_list = soup.select(".number-list li")

            items = soup.select(".announcement-container")
            if x > int(number_list[-1].text.strip()):
                break

            for item in items:
                link = "https://www.bazaraki.com" + item.select_one("a")['href']

                if link not in Product.links:
                    Product.links.append(link)
            logger.info(f"Collect link from page {x}")
        except Exception as err:
            logger.error(f"Err {err}. Wait: 15 sec", exc_info=True)
            time.sleep(WAIT)
            continue


def collect_data(cls: FunctionUnit):
    for e, link in enumerate(Product.links):
        try:
            Product(link)
            logger.info(f"Total: {len(Product.links)} Left: {len(Product.links) - e}.")
        except Exception as err:
            logger.error(f"Err {err}. Wait: {WAIT} sec", exc_info=True)
            Product.bad_urls.append(link)
            time.sleep(WAIT)
            continue


def report(cls: FunctionUnit):
    Report(Product.finally_data)


def main():
    unit01 = FunctionUnit(search_content)
    unit02 = FunctionUnit(collect_data)
    unit01.run()
    unit02.run()
    if Product.bad_urls:
        Product.links.clear()
        Product.links.extend(Product.bad_urls)
        unit02.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.debug("\n >>> Stop. CTRL+C")
    finally:
        unit03 = FunctionUnit(report)
        unit03.run()
        del requests
