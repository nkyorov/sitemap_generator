from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
from urllib.parse import urljoin, urlparse
import tldextract
import xml.etree.cElementTree as ET
from reppy.robots import Robots
import requests
import sys
import datetime
import random
import time
from GraphWriter import *
from proxyFinder import *

class Spider:
    urls_queue = set()
    crawled_urls = set()
    seed_url = ''
    seed_domain = ''
    crawled = 0
    listToXML = []
    delay = 0
    # Mode 0: Default
    # Mode 1: Polite
    # Mode 2: Aggressive
    proxy = False
    crawl_mode = 0 
    proxies = []    

    def __init__(self,url,limit=-1,depth_limit=-1,proxy=-1, crawl_mode=0):
        # Set fields
        Spider.seed_url = LinkExtractor.urlChecker(url)
        Spider.seed_domain = tldextract.extract(Spider.seed_url).registered_domain
        Spider.limit = limit
        Spider.crawl_mode = crawl_mode
        Spider.depth_limit = depth_limit
        
        # Get proxies, if flag is turned on
        if proxy == 1:
            Spider.proxies = ProxyList().getList()
            Spider.proxy = True

        # Set delays
        if Spider.crawl_mode == 0 or Spider.crawl_mode == 1:
            Spider.delay = Spider.getDelay()
            if Spider.delay is None:
                Spider.delay = 0
        else:
            Spider.delay = 0 

        Spider.urls_queue.add(Spider.seed_url)

        # Crawl until no URLs are left in the queue
        while Spider.urls_queue:
            for link in Spider.urls_queue.copy():  
                time.sleep(Spider.delay)
                Spider.crawl(link)
        # Create XML sitemap when done
        print(Spider.crawled)
        Spider.createXML()

    def crawl(page):
        # Crawl page if we haven't already
        if page not in Spider.crawled_urls:
            # Check limits
            if((Spider.crawled < Spider.limit) or Spider.limit==-1): 
                # Extract links
                LinkExtractor.extract(page)
                Spider.crawled_urls.add(page)
                Spider.urls_queue.discard(page)
                print("Crawling: " + page)
                Spider.crawled += 1
 
            # Crawl limit reached
            else:
                print(Spider.crawled)
                Spider.createXML()
                GraphWriter(list(Spider.crawled_urls))
                sys.exit("Maximum page limit reached!")
    
    # Finds the delay specified in robots.txt
    def getDelay():
        return Robots.fetch(Spider.seed_url + 'robots.txt').agent('*').delay
    
    # Checks if a URL is allowed    
    def checkRobots(url):
        robots = Robots.fetch(Spider.seed_url + 'robots.txt')
        agent = robots.agent('*')
        agent_str = str(agent)
        if len(agent_str) == 2:
            return True
        else:
            return agent.allowed(url)

    # Creates sitemap
    def createXML():
        xml = open('sitemap.xml','w')
        xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")

        for line in Spider.listToXML:
            xml.write("\t<url>\n")
            xml.write("\t\t<loc>%s</loc>\n" % line['url'])
            if line['last_mod'] != '*':
                xml.write("\t\t<lastmod>%s</lastmod>\n" % line['last_mod'])
            xml.write("\t</url>\n")
        xml.write("</urlset>")
        xml.close()
    
class LinkExtractor:
    def add_link(url,last_mod):
        SKIP = False        
        domain = tldextract.extract(url).registered_domain

        # Skip pages that are already crawled or are already in the queue
        if (url in Spider.crawled_urls) or (url in Spider.urls_queue):
            SKIP = True
        
        # Skip pages that are not in the same domain
        if not domain == Spider.seed_domain:
            SKIP = True
        
        # Skip pages that are above the depth limit
        if LinkExtractor.getDepth(url) > Spider.depth_limit and Spider.depth_limit != -1:
            SKIP = True

        if not SKIP:
            Spider.urls_queue.add(url)
            Spider.listToXML.append({'url':url,'last_mod':last_mod})

    def extract(page):
        if Spider.proxy:
            headers = ProxyList.getHeaders()
            proxy = ProxyList.getRandomProxy(Spider.proxies)
            random.shuffle(Spider.proxies)
            try:
                response = requests.get(page,proxies=proxy,headers=headers).text
            except:
                time.sleep(2)
                proxy = ProxyList.getRandomProxy(Spider.proxies)
                response = requests.get(page,proxies=proxy,headers=headers).text
        else:
            if Spider.crawl_mode == 1:
                start = time.time()
                response = requests.get(page).text
                end = time.time() - start
                Spider.delay = end * 2
            else:
                response = requests.get(page).text
        
        # Find last modification date
        header = requests.head(page).headers
        if 'Last-Modified' in header:
            last_mod = header['Last-Modified']
            
            # Convert to W3C Datetime format
            last_mod = datetime.datetime.strptime(last_mod, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            last_mod = '*'

        # Extract all <a></a> tags on the webpage
        for url in BeautifulSoup(response,parse_only=SoupStrainer('a'),features='html.parser'):
            if url.has_attr('href'):
                url = urljoin(page,url['href'])        
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