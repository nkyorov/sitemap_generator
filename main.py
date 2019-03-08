from Spider import *
import time

start = time.clock()
url = "http://toscrape.com"
Spider(url)

count = 0

while Spider.urls_queue:
    for link in Spider.urls_queue.copy():  
        Spider.crawl(link)

print("TOTAL TIME: " + str(time.clock()-start))
print("TOTAL PAGES: " + str(Spider.crawled))

