import datetime
import time
import os

from discord_logger import logger

from selenium.webdriver.firefox.options import Options

from database.model import Stock, SaleService

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import schedule


SOURCE_URL = os.environ.get('SOURCE_URL')
BASE_DIR = os.getcwd()


def session_start():
    global session
    engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
    session = sessionmaker(bind=engine)()


def session_close():
    global session
    session.close()

def get_chrome():
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

'''
if os.name == 'nt':
    print("nt base")
    options = Options()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")
    options.add_argument('--headless')
else:
    ChromeDriverManager().install()

    # Set up Chrome WebDriver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(
    #     "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")
    chrome_options.add_argument('--headless')

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.headless = True

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_driver = os.path.join(BASE_DIR, 'chromedriver_114_0_5735_16')

    # chrome_driver = '/usr/bin/google-chrome'  # lnx test
    # chrome_options._binary_location = chrome_driver
    # chrome_options.binary_location(chrome_driver)
    os.chmod(chrome_driver, 0o755)

'''

options = Options()
options.set_preference("general.useragent.override",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")
options.add_argument('--headless')


def update_stock_price(stock):
    target = f'{SOURCE_URL}/{stock.name}:{stock.service.name}'
    bw = None
    try:

        # if os.name == 'nt':
        bw = webdriver.Firefox(options=options)
        # else:
        #     bw = webdriver.Chrome(options=chrome_options, service=Service(executable_path=chrome_driver))
            # bw = webdriver.Chrome(options=chrome_options)

        bw.get(target)
        bw.set_window_rect(width=320, height=480)
        time.sleep(5)
        price = bw.find_element(By.XPATH,
                                '/html/body/c-wiz[2]/div/div[4]/div/main/div[2]/div[1]/c-wiz/div/div[1]/div/div[1]/div/div[1]/div/span/div/div')

        price = price.text.replace('₺', '')
        price = price.replace(',', '.')

        if stock.current_price == 0:
            percentage_change = ((int(stock.initial_price) - float(price)) / int(stock.initial_price)) * 100
            percentage_change_send_to_log(percentage_change, float(price), stock, float(price) >= stock.initial_price)
        else:
            percentage_change = ((int(stock.current_price) - float(price)) / int(stock.current_price)) * 100
            percentage_change_send_to_log(percentage_change, float(price), stock, float(price) >= stock.current_price)
        stock.current_price = float(price)
        session.commit()

    except Exception as error:
        logger.construct(
            title='get stock price',
            description='Price',
            metadata=str(error.__dict__).replace(',', '\n'),
            level='error'
        )
        # logger.send()
        # logger.remove_embed_msg()
        raise error
    finally:
        if bw is not None:
            bw.quit()


def get_task_list():
    global session
    return session.query(Stock).all()


def percentage_change_send_to_log(percentage, price, stock, way):
    if abs(percentage) > 2:
        logger.construct(
            level="success" if way else "error",
            description=f':{"chart_with_upwards_trend" if way else "chart_with_downwards_trend"}: '
                        f'Fiyat {"yükselişi" if way else "düşüşü"}'
                        f' {stock.name} {stock.current_price}to{price} | {abs(percentage):.2f}%"',
            metadata=f'{stock.name} {stock.current_price}to{price} | {abs(percentage):.2f}% |'
                     f' investment({stock.initial_price * stock.purchase_quantity}) '
                     f'- middle({stock.current_price * stock.purchase_quantity})'
                     f'- gain({price * stock.purchase_quantity})'
        )


def stock_available_information_task(stock):
    df = stock.date_flow
    s, e, n = df.request_start_date, df.request_end_date, datetime.datetime.now().date()
    logger.construct(
        title=f'Stock is available {stock.name}',
        description=f'{stock.name} | {s}<{n}<{e}',
        metadata=f'Start {s} < End {e} | NOW : {n}'
    )
    logger.send()


def stock_price_flower():
    session_start()

    for stock in get_task_list():
        if datetime.datetime.now().date() >= stock.date_flow.process_start_date and stock.process:

            print(f'stock scraper start - {stock.name}')
            update_stock_price(stock)
            print(f'stock scraper end - {stock.name}')

    session_close()

    try:
        if len(logger.discord.get_embeds()) > 0:
            logger.send()
        logger.remove_embed_msg()
    except:
        pass

def stock_available_flower():
    session_start()
    for stock in get_task_list():
        df = stock.date_flow
        s, e, n = df.request_start_date, df.request_end_date, datetime.datetime.now().date()
        if s <= n <= e:
            stock_available_information_task(stock)
    session_close()


def send_wake_log(*args, **kwargs):
    from time import gmtime, strftime
    job_text = '\n'.join(kwargs.get('job_list', []))
    logger.construct(
        title='Service is woke',
        metadata=f'os name {os.name} - tz {strftime("%z", gmtime())}\n'
                 f'Tasks:\n{job_text}\n'
                 f'chrome {get_chrome()}'
    )
    logger.send()
    logger.remove_embed_msg()


def main():
    task_list_information = []

    # stock price flow
    schedule.every().day.at(f"{8-3:02}:10").do(stock_price_flower)
    task_list_information.append(f'08:10 - stock_price_flower')
    for hour in range(9, 18):
        schedule.every().day.at(f"{hour-3:02}:00").do(stock_price_flower)
        task_list_information.append(f"{hour:02}:00 - stock_price_flower")

    # stock available flow
    schedule.every().day.at(f'{10-3:02}:50').do(stock_available_flower)
    task_list_information.append(f"{10:02}:00 - stock_available_flower")

    send_wake_log(job_list=task_list_information)

    if bool(os.environ.get('DEBUG')):
        print("debug")
        stock_price_flower()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
else:
    logger.construct(
        title='non mian'
    )
    logger.send()

