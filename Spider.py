from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
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
            add_link(url['href'])

def crawl(page):
    if page not in crawled_urls:
        extract(page)
        urls_queue.remove(page)



# Tests
# print("----------------------------------------")
# urls_queue.add("http://toscrape.com")
# print(urls_queue)

# add_link("http://dev.toscrape.com")
# add_link("http://not.a.link.toscrape.com")
# add_link("http://google.com")
# add_link("http://adsasdaf.com")
# add_link("http://efu3r13re.com")
# add_link("http://toscrape.com/ad/gg/23/")

# print("----------------------------------------")
# print(urls_queue)

