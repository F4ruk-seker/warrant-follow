from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from database import currently_queries as cq
from pydantic import BaseModel, types
from datetime import datetime


class StockAPIModel(BaseModel):
    name: str
    initial_price: float
    current_price: float
    purchase_quantity: int
    process: bool

    request_start_date: str
    request_end_date: str
    process_start_date: str

    sale_service_id: int


app = FastAPI()

origins = ["https://finance.darken.gen.tr/", "https://finance.darken.gen.tr"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sale_service_list/")
async def sale_services():
    return cq.sale_service_list()


@app.get("/stock_list/")
async def sale_services():
    return cq.stock_list()


@app.post("/stock/")
async def create_stock(data: StockAPIModel):
    print(data)
    '''
    name = Column(String)
    initial_price = Column(Float)
    current_price = Column(Float)
    purchase_quantity = Column(Integer)
    process = Column(Boolean)

    :param data:
    :return:
    '''
    _date = cq.create_date(date={
        "request_start_date": data.request_start_date,
        "request_end_date": data.request_end_date,
        "process_start_date": data.process_start_date
    })

    stock_data = {
        'name': data.name,
        'initial_price': data.initial_price,
        'current_price': data.current_price,
        'purchase_quantity': data.purchase_quantity,
        'process': data.process,
        # '__service_id': data.sale_service_id,
        '__service_id': 2,
        # '__date_flow_id': _date.id
        '__date_flow_id': 1
    }

    cq.add_stock(stock=stock_data)
    # You can return a response indicating success or the newly created stock ID
    return {"message": "Stock created successfully"}

