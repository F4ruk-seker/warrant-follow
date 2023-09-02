if __name__ == '__main__':
    from utils import session_handle
    from model import Stock, SaleService, DateFlow
else:
    from .utils import session_handle
    from .model import Stock, SaleService, DateFlow


@session_handle
def stock_list(session):
    return session.query(Stock).all()


@session_handle
def add_stock(session, **kwargs):
    s = Stock()
    for k in Stock.__dict__.keys():
        setattr(s, k, kwargs.get('stock').get(k, None))
    return s


@session_handle
def create_date(session, **kwargs):
    from datetime import datetime

    s = DateFlow()

    date_data = kwargs.get('date', {})

    for key, value in date_data.items():
        if hasattr(s, key):
            d = datetime.strptime(value, "%Y-%m-%d").date()
            setattr(s, key, d)
        else:
            pass

    session.add(s)
    session.commit()
    return s


@session_handle
def sale_service_list(session):
    return session.query(SaleService).all()

