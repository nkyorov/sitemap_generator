import requests
import urllib.request
import httplib2
import secrets
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
        ip, index= getRandomProxy(proxies)
        userAgent = UserAgent().random
        headers ={'User-Agent':userAgent}
        proxy = {"http":"http://" + ip,"https":"http://" + ip}
        response = requests.get("http://buzzfeed.com",proxies=proxy,timeout=2,headers=headers)
        if(response.status_code == 200):
            print("Request successful: " + ip)
            print(len(proxies))
    except:
        #print("Removing: " + str(proxies[index]))
        del proxies[index]