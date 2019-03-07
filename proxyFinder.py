import requests
import urllib.request
import httplib2
import secrets
from bs4 import BeautifulSoup


def getListOfProxies():
    proxies = []
    
    url = 'https://www.sslproxies.org/'

    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response,'html.parser')

    table = soup.find(id='proxylisttable')

    for row in table.tbody.find_all('tr'):
        proxies.append({
        'ip':   row.find_all('td')[0].string,
        'port': row.find_all('td')[1].string
    })
    return proxies


def getRandomProxy(list):
    i = secrets.randbelow(len(proxies))
    return proxies[i]

# proxies = getListOfProxies()
# proxy = getRandomProxy(proxies)
# print(proxy)