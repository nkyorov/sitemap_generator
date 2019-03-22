from Spider import *
import click

@click.command()
@click.argument('url')
@click.option("--limit", help="Number of greetings.")
@click.option("--depth", help="Number of greetings.")

def crawl(url,limit, depth):
    if(bool(urlparse(url).scheme)):
        pass
    else:
        url = 'http://' + url
    
    if limit is None:
        limit = -1
    if depth is None:
        depth = -1 

    Spider(url,limit,depth)
    while Spider.urls_queue:
        for link in Spider.urls_queue.copy():  
            Spider.crawl(link)
    

if __name__ == '__main__':
    crawl()