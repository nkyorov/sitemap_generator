import requests
import urllib.request
import httplib2
import secrets
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

class ProxyList:

    def __init__(self):
        print("Testing proxies\n\n")
        self.proxies = ProxyList.testProxies()

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
        return proxy

    def testProxies():
        proxies = ProxyList.getListOfProxies()
        working_proxies = []
        for proxy in proxies:
            ip = proxy['ip'] + ":" + proxy['port']
            userAgent = UserAgent().random
            headers ={'User-Agent':userAgent}
            proxy = {"http":"http://" + ip,"https":"http://" + ip}
            try:
                response = requests.get("http://buzzfeed.com",proxies=proxy,timeout=2,headers=headers)
                if(response.status_code == 200):
                    print("Request successful: " + ip)
                    working_proxies.append(proxy)
            except:
                print("Request unsuccessful. Trying next proxy.")
            
        return working_proxies

    def getHeaders():
        userAgent = UserAgent().random
        headers = {'User-Agent':userAgent}
        return headers

    def getList(self):
        return self.proxies

