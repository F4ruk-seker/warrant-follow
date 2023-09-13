import json

from task.task_base import TaskBase
from scraper.d_scraper import scraper_config
from scraper.d_scraper.test_scraper import Scraper
import config


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
                try:
                    return json.loads(old_frame.read())
                except json.decoder.JSONDecodeError:
                    old_frame.close()
                    os.remove(self.old_data_path)
        return {}

    def save_new_data(self, data):
        with open(self.old_data_path, 'w') as old_frame:
            old_frame.write(json.dumps(data))

    @staticmethod
    def get_new_data():
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

t = SYNCFinanceAPI()
t.do()
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)