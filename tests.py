print("----------------------------------------")
urls_queue.add("http://toscrape.com")
print(urls_queue)

add_link("http://dev.toscrape.com")
crawled_urls.add("http://not.a.link.toscrape.com")
add_link("http://dev.toscrape.com")
add_link("http://admin.toscrape.com")
add_link("http://mod.toscrape.com")
add_link("http://toscrape.com/ad/gg/23/")

print("----------------------------------------")
print(urls_queue)
print("----------------------------------------")
crawl("http://not.a.link.toscrape.com")
print(urls_queue)
print(crawled_urls)




================
crawl(seed_url)
while urls_queue:
    for url in urls_queue.copy():
        crawl(url)

print(crawled_urls)
print("V")
print(urls_queue)

===========
crawl(seed_url)
print(urls_queue)
print(crawled_urls)
===========