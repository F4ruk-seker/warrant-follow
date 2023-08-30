import os
from discord_logger import logger

from database.model import Stock, SaleService, DateFlow

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
session = sessionmaker(bind=engine)()


def get_sale_service_list():
    for sale_service in session.query(SaleService).all():
        print(f'id: {sale_service.id} - {sale_service.name}')


def create_new_sale_service():
    code = input('Sale service code : ')
    for let, det in [
        ('ı', 'i'),
        ('ş', 's'),
        ('ç', 'c'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
    ]:
        code = code.replace(let, det)
    code = code.upper()
    sale_service = SaleService()
    sale_service.name = code

    if not session.query(SaleService).filter_by(name=code).count() > 0:
        session.add(sale_service)
        session.commit()


def create_new_stock():
    ...

