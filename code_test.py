
from requests import api


r = api.post('http://127.0.0.1:8000/stock/', json={
    "name": "PARS",
    "initial_price": "10",
    "current_price": "20",
    "purchase_quantity": "10",
    "process": "True"
})


print(r)
print(r.status_code)
print(r.text)
print(r.json())