from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import httplib2
from urllib.parse import urljoin, urlparse
import tldextract
import xml.etree.cElementTree as ET
from reppy.robots import Robots
import requests
import sys
import time
from GraphWriter import *

class Spider:
    urls_queue = set()
    crawled_urls = set()
    seed_url = ''
    seed_domain = ''
    crawled = 0
    listToXML = []
    delay = 0    

    def __init__(self,url,limit=-1,depth_limit=-1):
        Spider.seed_url = LinkExtractor.urlChecker(url)
        Spider.seed_domain = tldextract.extract(Spider.seed_url).registered_domain
        Spider.limit = limit
        Spider.depth_limit = depth_limit
        Spider.delay = Spider.getDelay()
        if Spider.delay is None:
            Spider.delay = 0
        Spider.urls_queue.add(Spider.seed_url)

        while Spider.urls_queue:
            for link in Spider.urls_queue.copy():  
                time.sleep(Spider.delay)
                Spider.crawl(link)
        
        Spider.createXML()

    def crawl(page):
        if page not in Spider.crawled_urls:
            if((Spider.crawled < Spider.limit) or Spider.limit==-1): 
                LinkExtractor.extract(page)
                Spider.crawled_urls.add(page)
                Spider.urls_queue.discard(page)
                print("Crawling: " + page)
                Spider.crawled += 1
            else:
                print(Spider.crawled)
                Spider.createXML()
                GraphWriter(list(Spider.crawled_urls))
                sys.exit("Maximum page limit reached!")

    def getDelay():
        return Robots.fetch(Spider.seed_url + 'robots.txt').agent('*').delay
        
    def checkRobots(url):
        robots = Robots.fetch(Spider.seed_url + 'robots.txt')
        agent = robots.agent('*')
        agent_str = str(agent)
        if len(agent_str) == 2:
            return True
        else:
            return agent.allowed(url)

    def createXML():
        xml = open('sitemap.xml','w')
        xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")

        for line in Spider.listToXML:
            xml.write("\t<url>\n")
            xml.write("\t\t<loc>%s</loc>\n" % line['url'])
            if line['last_mod'] != '*':
                xml.write("\t\t<lastmod>%s</lastmod>\n" % line['last_mod'])
            xml.write("\t\t<priority>0.5</priority>\n")
            xml.write("\t</url>\n")
        xml.write("</urlset>")
        xml.close()
    
class LinkExtractor:
    def add_link(url,last_mod):
        SKIP = False        
        domain = tldextract.extract(url).registered_domain

        if (url in Spider.crawled_urls) or (url in Spider.urls_queue):
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