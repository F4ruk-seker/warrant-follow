import requests


r = requests.get('https://protein7.com/3680-home_default/xpro-bcaa-glutamine-600gr.jpg')
print(r.url)
print(r.history)
print(r.cookies)
print(r.is_redirect)