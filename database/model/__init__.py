import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base


# Create a base class
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'Stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    initial_price = Column(Float)
    current_price = Column(Float)
    purchase_quantity = Column(Integer)
    process = Column(Boolean)

    __service_id = Column(Integer, ForeignKey('SaleServices.id'))
    service = relationship("SaleService")

    __date_flow_id = Column(Integer, ForeignKey('DateFlows.id'))
    date_flow = relationship('DateFlow')

    @property
    def sale_service(self):
        return self.service

    @classmethod
    def pre_load(cls, json):
        cls.__dict__.update(json)


class SaleService(Base):
    __tablename__ = 'SaleServices'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class DateFlow(Base):
    __tablename__ = 'DateFlows'
    id = Column(Integer, primary_key=True)

    request_start_date = Column(Date, nullable=True)
    request_end_date = Column(Date, nullable=True)

    process_start_date = Column(Date, nullable=True)


if __name__ == '__main__':
    import os
    from sqlalchemy import create_engine

    engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
    # Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    # for stock in session.query(Stock).all():
    #     print(stock.service.name)
    date = DateFlow()
    date.process_start_date = datetime.datetime.now().date()
    date.request_end_date = datetime.datetime.now().date()
    date.request_start_date = datetime.datetime.now().date()
    session.add(date)
    session.commit()

    session.close()
