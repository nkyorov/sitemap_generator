from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
from urllib.parse import urljoin
import tldextract

# def get_domain(url):
#     domain = tldextract.extract(url).registered_domain
#     return domain


urls_queue = set()
crawled_urls = set()
seed_url = "http://toscrape.com"
seed_domain = tldextract.extract(seed_url).registered_domain

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
            url = urljoin(seed_domain,url['href'])
            add_link(url)

def crawl(page):
    if page not in crawled_urls:
        extract(page)
        crawled_urls.add(page)
        urls_queue.discard(page)
