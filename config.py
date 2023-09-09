from models import ApiHostModel
from pathlib import Path
import environ


BASE_DIR = Path(__file__).resolve().parent

ENV = environ.Env()
environ.Env.read_env(BASE_DIR)

SYNC_URL = ApiHostModel(ENV('SCRAPER_SYNC_URL'), end=True)
SYNC_TOKEN = ENV('SCRAPER_SYNC_TOKEN')

FINANCE_DATA_SOURCE_URL = ApiHostModel(ENV('SOURCE_URL'), end=False)

DEBUG = True

