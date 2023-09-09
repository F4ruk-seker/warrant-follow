from requests import api
from http import HTTPStatus
from config import *
from models.scraper_model import ScraperModel


class ScraperManager:
    def __init__(self):
        self.__work_range: None = None
        self.__response_status = False

    def __get_scraper(self):
        if response := api.get(SYNC_URL / SYNC_TOKEN):
            self.__response_status = bool(response)
            return ScraperModel(response.json())

    def __bool__(self):
        return self.__response_status

    def __call__(self, *args, **kwargs) -> ScraperModel:
        return self.__get_scraper()



