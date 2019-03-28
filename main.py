from Spider import *
import click

@click.command()
@click.argument('url')
@click.option("--limit", type=int, help="Limit the crawler, until that number is reached.")
@click.option("--depth", type=int, help="Crawl until this level.")

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


if __name__ == '__main__':
        crawl()
