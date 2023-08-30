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
options.add_argument('--headless')


def get_stock_price(target):
    try:
        bw = webdriver.Firefox(options=options)
        bw.get(target)
        time.sleep(2)
        price = bw.find_element(By.XPATH,
                                '/html/body/c-wiz[2]/div/div[4]/div/main/div[2]/div[1]/div[1]/c-wiz/div/div[1]/div/div[1]/div/div[1]/div/span/div/div')

        price = price.text.replace('₺', '')
        price = price.replace(',', '.')
        return float(price)

    except Exception as error:
        logger.construct(
            title='get stock price',
            description='Price',
            metadata=str(error.__dict__).replace(',', '\n'),
            level='error'
        )
    finally:
        bw.quit()


def get_task_list():
    global session
    return session.query(Stock).all()


def percentage_change_send_to_log(percentage, price, stock, way):
    if abs(percentage) > 2:
        logger.construct(
            level='info',
            description=f':chart_with_downwards_trend: Fiyat {"yükselişi" if way else "düşüşü"}'
                        f' {stock.name} {stock.current_price}to{price} | {abs(percentage):.2f}%"',
            metadata=f'{stock.name} {stock.current_price}to{price} | {abs(percentage):.2f}% |'
                     f' investment({stock.initial_price * stock.purchase_quantity}) '
                     f'- gain({price * stock.purchase_quantity})'
        )


def task():
    for stock in get_task_list():
        target = f'{SOURCE_URL}/{stock.name}:{stock.sale_service[0].name}'

        price = get_stock_price(target)

        percentage_change = ((stock.current_price - price) / stock.current_price) * 100

        percentage_change_send_to_log(percentage_change, price, stock, stock.current_price >= price)
        stock.current_price = price
        session.commit()
    try:
        if len(logger.discord.get_embeds()) >= 1:
            logger.send()
    except:
        pass


def main():
    schedule.every().day.at(f"{7:02}:39").do(task)
    # for hour in range(9, 18):
    #     schedule.every().day.at(f"{hour:02}:00").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
