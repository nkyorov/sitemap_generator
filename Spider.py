from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
import tldextract

urls_queue = set()
crawled_urls = set()
base_url = "http://toscrape.com"
domain = get_domain(base_url)

def get_domain(url):
    registered_domain = tldextract.extract(url).registered_domain
    return registered_domain

def add_link(url):
    FLAG_1 = False
    FLAG_2 = False

    if(url in urls_queue) or (url in crawled_urls):
        FLAG_1 = True
    
    if not FLAG_1:
        urls_queue.add(url)


def extract(page):
    http = httplib2.Http()
    status, response = http.request(page)
            
    for url in BeautifulSoup(response,parse_only=SoupStrainer('a'),features='html.parser'):
        if url.has_attr('href'):
            add_link(url['href'])
    

extract(base_url)
print(urls_queue)


print(get_domain('http://forums.bbc.co.uk'))