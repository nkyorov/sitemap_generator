from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
from urllib.parse import urljoin
import tldextract
import xml.etree.cElementTree as ET
from reppy.robots import Robots

urls_queue = set()
crawled_urls = set()
seed_url = "http://toscrape.com"
seed_domain = tldextract.extract(seed_url).registered_domain


def checkRobots(url):
    robots = Robots.fetch(seed_url + '/robots.txt')
    return robots.allowed(url,'*')


def add_link(url):
    NOT_SEEN = True
    SAME_DOMAIN = True
    
    # Passed url domain
    domain = tldextract.extract(url).registered_domain

    if(url in urls_queue) or (url in crawled_urls):
        NOT_SEEN = False
    
    if not domain == seed_domain:
        SAME_DOMAIN = False

    if NOT_SEEN and SAME_DOMAIN:
        urls_queue.add(url)

def extract(page):
    http = httplib2.Http()
    status, response = http.request(page)
            
    for url in BeautifulSoup(response,parse_only=SoupStrainer('a'),features='html.parser'):
        if url.has_attr('href'):
            url = urljoin(page,url['href'])
            add_link(url)

def crawl(page):
    if page not in crawled_urls and checkRobots(page):
        extract(page)
        crawled_urls.add(page)
        urls_queue.discard(page)

crawl(seed_url)


url_copy = urls_queue.copy()
while urls_queue:
    for url in urls_queue.copy():
        print("Crawling: " + url)    
        crawl(url)
