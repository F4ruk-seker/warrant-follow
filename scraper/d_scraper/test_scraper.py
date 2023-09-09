import json
import time

import requests
from bs4 import BeautifulSoup
import re

import config


class Price:
    """
    CUSTOM INT OBJ FOR DATA SOURCE
    """

    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return self.obj

    def __int__(self):
        if type(self.obj) is str:
            return int(self.obj.split(',')[0].replace('.', ''))
        return int(self.obj)

    def __float__(self):
        if type(self.obj) is str:
            pyload = self.obj.split(',')
            if len(pyload) == 1:
                h, d = int(self.obj.split(',')[0].replace('.', '')), 00  # lok af , to .
            elif len(pyload) == 2:
                h, d = int(self.obj.split(',')[0].replace('.', '')), int(self.obj.split(',')[1][:2])
            else:
                raise 'unknown string format'
            return float(f'{h}.{d}')
        return float(self.obj)


def rate(rate_str) -> str:
    pattern = r'([0-9,]+)'
    match = re.search(pattern, rate_str)
    if match:
        return match.group(0)
    return ''


class Scraper(object):
    def __init__(self, target: str):
        self.target = target
        self.__result = []
        self.scraper()

    def scraper(self):
        if response := requests.get(self.target):
            pyload = BeautifulSoup(response.text, 'html.parser')
            stock_table = pyload.find('table', {"id": "stocks"})
            stock_table_body = stock_table.find('tbody')
            for stock_frame in stock_table_body.find_all('tr'):
                stock_pyload = stock_frame.find_all('td')
                self.__result.append({
                    'logo': stock_pyload[0].find('img')['data-src'],
                    'code': stock_pyload[0].find_all('div')[1].text,
                    'expansion': stock_pyload[0].find_all('div')[2].text,
                    'last_price': float(Price(stock_pyload[1].text)),
                    'change_rate': rate(stock_pyload[5].text),
                    'last_update_time': stock_pyload[6].text
                })

    def __len__(self):
        return len(self.__result)

    @property
    def result(self):
        return self.__result


## task

class TaskBase:
    def __init__(self):
        self.__errors = []

    @property
    def has_error(self):
        return len(self.__errors) > 0

    @property
    def get_errors(self) -> list:
        return self.__errors

    def do(self):
        ...


class SYNCFinanceAPI(TaskBase):
    """

    """
    def __init__(self):
        super().__init__()
        self.old_data_path_name = 'old_finance_data.json'
        self.old_data_path = config.BASE_DIR / self.old_data_path_name

    @staticmethod
    def to_df(data):
        return pd.DataFrame(data)

    def get_old_data(self):
        if os.path.isfile(self.old_data_path):
            with open(self.old_data_path, 'r+') as old_frame:
                return json.loads(old_frame.read())
        return {}

    def save_new_data(self, data):
        with open(self.old_data_path, 'w') as old_frame:
            old_frame.write(json.dumps(data))

    def get_new_data(self):
        scraper = Scraper(scraper_config.DATA_SOURCE_URL)
        return scraper.result

    def update_api(self):
        ...

    def do(self):
        if updates := self.get_updates():
            print(updates)

    def get_updates(self):
        old_data = self.get_old_data()
        new_data = self.get_new_data()
        old = pd.DataFrame(old_data)
        new = pd.DataFrame(new_data)
        differences = new[~new.isin(old)].dropna()
        self.save_new_data(new_data)
        return differences.to_dict(orient='records')


import pandas as pd
import os
import scraper_config

t = SYNCFinanceAPI()
t.do()



# s = Scraper(scraper_config.DATA_SOURCE_URL)
# time.sleep(1)
# d = Scraper(scraper_config.DATA_SOURCE_URL)
#
# old = pd.DataFrame(s.result)
# new = pd.DataFrame(d.result)
#
# differences = new[~new.isin(old)].dropna()
# # must be empty
# print(differences)

# differences_json = differences.to_dict(orient='split')
#
# # JSON verisini yazdırın veya kullanın
# print(differences_json.get('data'))