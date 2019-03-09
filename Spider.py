from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
from urllib.parse import urljoin
import tldextract
import xml.etree.cElementTree as ET
from reppy.robots import Robots
import requests
import sys

class Spider:
    urls_queue = set()
    crawled_urls = set()
    seed_url = ''
    seed_domain = ''
    crawled = 0
    limit = 0
    listToXML = []

    def __init__(self,url,limit):
        Spider.seed_url = Spider.urlChecker(url)
        Spider.seed_domain = tldextract.extract(self.seed_url).registered_domain
        Spider.limit = limit
        Spider.crawl(self.seed_url)

    def crawl(page):
        if page not in Spider.crawled_urls:
            if(Spider.crawled < Spider.limit): 
                Spider.extract(page)
                Spider.crawled_urls.add(page)
                Spider.urls_queue.discard(page)
                print("Crawling: " + page)
                Spider.crawled += 1
            else:
                print(Spider.listToXML)
                sys.exit("Maximum page limit reached!")


    def checkRobots(url):
        robots = Robots.fetch(Spider.seed_url + 'robots.txt')
        agent = robots.agent('*')
        agent_str = str(agent)
        if len(agent_str) == 2:
            return True
        else:
            return agent.allowed(url)


    def add_link(url,last_mod):
        NOT_SEEN = True
        SAME_DOMAIN = True
        
        domain = tldextract.extract(url).registered_domain

        if(url in Spider.urls_queue) and (url in Spider.crawled_urls):
            NOT_SEEN = False
        
        if not domain == Spider.seed_domain:
            SAME_DOMAIN = False

        if NOT_SEEN and SAME_DOMAIN:
            Spider.urls_queue.add(url)
            Spider.listToXML.append({'url':url,'last_mod':last_mod})

    def extract(page):
        response = requests.get(page).text
        header = requests.head(page).headers
        if 'Last-Modified' in header:
            last_mod = header['Last-Modified']
        else:
            last_mod = 'Not available'
        for url in BeautifulSoup(response,parse_only=SoupStrainer('a'),features='html.parser'):
            if url.has_attr('href'):
                url = urljoin(page,url['href'])
                url = Spider.urlChecker(url)                
                Spider.add_link(url,last_mod)

    def urlChecker(url):
        if url.endswith('/'):
            return url
        else:
            url += '/'
            return url
   