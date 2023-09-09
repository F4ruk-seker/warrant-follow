import os
import time

from selenium.webdriver.common.by import By

import scraper_config
import config

from selenium.webdriver.firefox.options import Options as FirefoxOption
from selenium import webdriver


class SCRAPER_BROWSERES:
    firefox = "firefox"
    chrome = "chrome"


def get_chrome_path():
    if os.path.isfile('/usr/bin/chromium-browser'):
        return '/usr/bin/chromium-browser'
    elif os.path.isfile('/usr/bin/chromium'):
        return '/usr/bin/chromium'
    elif os.path.isfile('/usr/bin/chrome'):
        return '/usr/bin/chrome'
    elif os.path.isfile('/usr/bin/google-chrome'):
        return '/usr/bin/google-chrome'
    else:
        return None


def get_browser():
    if scraper_config.SCRAPER_BROWSER == SCRAPER_BROWSERES.firefox:
        options = FirefoxOption()
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

        if not config.DEBUG:
            options.add_argument('--headless')
        return webdriver.Firefox(options=options)


class Scraper:
    def __init__(self, target: str):
        self.result = None
        self.target = target
        self.wait_for_load_delay_time = 0
        self.scraper()

    def scraper(self):
        bw = None
        try:
            bw = get_browser()
            bw.set_window_rect(width=320, height=480)
            bw.get(self.target)
            time.sleep(self.wait_for_load_delay_time)
            self.result = bw.find_element(By.XPATH, scraper_config.x_path)
            self.result = self.result.text.replace('₺', '')
            self.result = self.result.replace(',', '.')
        except Exception as e:
            # if not self.wait_for_load_delay_time > 5:
            #     self.wait_for_load_delay_time += 1
            #     self.scraper()
            print(e)
            ...  # log
        finally:
            if bw is not None:
                bw.close()

    def __bool__(self):
        return self.result is not None

    def __float__(self):
        return float(self.result)

    def __int__(self):
        return int(self.result.split('.')[0])

