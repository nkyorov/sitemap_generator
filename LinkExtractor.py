import tldextract
from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.parse import urljoin, urlparse
from Spider import Spider

class LinkExtractor:
    def add_link(url,last_mod):
        SKIP = False        
        domain = tldextract.extract(url).registered_domain

        if url in Spider.crawled_urls:
            SKIP = True
        
        if not domain == Spider.seed_domain:
            SKIP = True
        
        if LinkExtractor.getDepth(url) > Spider.depth_limit and Spider.depth_limit != -1:
            SKIP = True

        if not SKIP:
            Spider.urls_queue.add(url)
            Spider.listToXML.append({'url':url,'last_mod':last_mod})

    def extract(page):
        response = requests.get(page).text
        header = requests.head(page).headers
        if 'Last-Modified' in header:
            last_mod = header['Last-Modified']
        else:
            last_mod = '*'
        for url in BeautifulSoup(response,parse_only=SoupStrainer('a'),features='html.parser'):
            if url.has_attr('href'):
                url = urljoin(page,url['href'])
                url = LinkExtractor.urlChecker(url)                
                LinkExtractor.add_link(url,last_mod)

    def urlChecker(url):
        if url.endswith('/'):
            return url
        else:
            url += '/'
            return url

    def getDepth(url):
        url = urlparse(url).path
        return url.count('/') - 1