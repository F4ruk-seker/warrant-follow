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

import schedule


engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
session = sessionmaker(bind=engine)()


SOURCE_URL = os.environ.get('SOURCE_URL')

options = Options()
options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")
options.add_argument('--headless')


def update_stock_price(stock):
    target = f'{SOURCE_URL}/{stock.name}:{stock.service.name}'
    bw = None
    try:

        bw = webdriver.Firefox(options=options)
        bw.get(target)
        bw.set_window_rect(width=320, height=480)
        time.sleep(5)
        price = bw.find_element(By.XPATH,
                                '/html/body/c-wiz[2]/div/div[4]/div/main/div[2]/div[1]/c-wiz/div/div[1]/div/div[1]/div/div[1]/div/span/div/div')

        price = price.text.replace('₺', '')
        price = price.replace(',', '.')

        if stock.current_price == 0:
            percentage_change = ((int(stock.initial_price) - float(price)) / int(stock.initial_price)) * 100
            percentage_change_send_to_log(percentage_change, float(price), stock, stock.initial_price >= float(price))
        else:
            percentage_change = ((int(stock.current_price) - float(price)) / int(stock.current_price)) * 100
            percentage_change_send_to_log(percentage_change, float(price), stock, stock.current_price >= float(price))
        stock.current_price = float(price)
        session.commit()


        try:
            if len(logger.discord.get_embeds()) > 0:
                logger.send()
        except:
            pass

    except Exception as error:
        logger.construct(
            title='get stock price',
            description='Price',
            metadata=str(error.__dict__).replace(',', '\n'),
            level='error'
        )
    finally:
        if bw is not None:
            bw.quit()


def get_task_list():
    global session
    return session.query(Stock).all()


def percentage_change_send_to_log(percentage, price, stock, way):
    if abs(percentage) > 2:
        logger.construct(
            level="info" if way else "error",
            description=f':chart_with_downwards_trend: Fiyat {"yükselişi" if way else "düşüşü"}'
                        f' {stock.name} {stock.current_price}to{price} | {abs(percentage):.2f}%"',
            metadata=f'{stock.name} {stock.current_price}to{price} | {abs(percentage):.2f}% |'
                     f' investment({stock.initial_price * stock.purchase_quantity}) '
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
    for stock in get_task_list():
        if datetime.datetime.now().date() >= stock.date_flow.process_start_date:
            update_stock_price(stock)


def stock_available_flower():
    for stock in get_task_list():
        df = stock.date_flow
        s, e, n = df.request_start_date, df.request_end_date, datetime.datetime.now().date()
        if s <= n <= e:
            stock_available_information_task(stock)


def send_wake_log():
    logger.construct(
        title='Service is woke'
    )


def main():
    send_wake_log()
    # stock price flow
    schedule.every().day.at(f"{8:02}:10").do(stock_price_flower)
    for hour in range(9, 18):
        schedule.every().day.at(f"{hour:02}:00").do(stock_price_flower)

    # stock available flow
    schedule.every().day.at(f'{10:02}:50').do(stock_available_flower)

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