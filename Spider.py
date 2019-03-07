from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
from urllib.parse import urljoin
import tldextract
import xml.etree.cElementTree as ET
from reppy.robots import Robots


class Spider:
    urls_queue = set()
    crawled_urls = set()
    seed_url = ''
    seed_domain = ''

    def __init__(self,url):
        Spider.seed_url = url
        Spider.seed_domain = tldextract.extract(self.seed_url).registered_domain
        Spider.crawl(self.seed_url)

    def crawl(page):
        if page not in Spider.crawled_urls:
            Spider.extract(page)
            Spider.crawled_urls.add(page)
            Spider.urls_queue.discard(page)
            print("Crawling: " + page)

    def checkRobots(url):
        robots = Robots.fetch(Spider.seed_url + '/robots.txt')
        return robots.allowed(url,'*')


    def add_link(url):
        NOT_SEEN = True
        SAME_DOMAIN = True
        
        # Passed url domain
        domain = tldextract.extract(url).registered_domain

        if(url in Spider.urls_queue) or (url in Spider.crawled_urls):
            NOT_SEEN = False
        
        if not domain == Spider.seed_domain:
            SAME_DOMAIN = False

        if NOT_SEEN and SAME_DOMAIN:
            Spider.urls_queue.add(url)

    def extract(page):
        http = httplib2.Http()
        status, response = http.request(page)
        for url in BeautifulSoup(response,parse_only=SoupStrainer('a'),features='html.parser'):
            if url.has_attr('href'):
                url = urljoin(page,url['href'])
                Spider.add_link(url)

