import requests
import urllib.request
import httplib2
import secrets
import requests
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


def getRandomProxy(proxies):
    i = secrets.randbelow(len(proxies))
    proxy = proxies[i]
    ip = proxy['ip'] + ":" + proxy['port']
    return ip,i

proxies = getListOfProxies()
ip, index= getRandomProxy(proxies)

while True:
    try:
        proxy, index= getRandomProxy(proxies)
        p = {"http":"http://" + proxy,"https":"http://" + proxy}
        r = requests.get("http://icanhazip.com",proxies=p,timeout=2)
        if(r.status_code == 200):
            print(r.text)
    except:
        print("Removing: " + str(proxies[index]))
        del proxies[index]
        print("DONE")
