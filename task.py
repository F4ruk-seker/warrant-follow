# import config
from requests import api

import config
import redis


class StockList(list):
    def __init__(self):
        super().__init__(self.stock_list)

    @property
    def stock_list(self):
        if response := api.get(config.SYNC_URL / config.SYNC_TOKEN + 'stock/'):
            return response.json()
        return []


def get_stock_new_price(stock):
    ...


# Bağlantı URL'sini ayarlayın
url = "redis://192.168.0.109:6379"

# Kullanıcı adı ve şifreyi ayarlayın
username = "pars"
password = "mypassword"

# Bir Redis nesnesi oluşturun
redis_client = redis.Redis(host="192.192.0.109", password='mypassword', username='pars')

# Redis sunucusuna bağlanın
redis_client.ping()

print("ok")