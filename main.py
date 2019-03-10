from Spider import *
import time

url = "http://toscrape.com"
Spider(url,2000,2)

while Spider.urls_queue:
    for link in Spider.urls_queue.copy():  
        Spider.crawl(link)
