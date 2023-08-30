from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
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

    sale_service = relationship("SaleService", back_populates="stock")


class SaleService(Base):
    __tablename__ = 'SaleServices'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    stock_id = Column(Integer, ForeignKey('Stocks.id'))

    stock = relationship("Stock", back_populates="sale_service")


if __name__ == '__main__':
    import os
    from sqlalchemy import create_engine

    engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
    Base.metadata.create_all(engine)
