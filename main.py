from Spider import *
import click

@click.command()
@click.argument('url')
@click.option("--limit", type=int, help="Limit the crawler, until that number is reached.")
@click.option("--depth", type=int, help="Crawl until this level.")
@click.option("--proxies", is_flag=True, help="Turn on proxies")
@click.option('--crawl_mode', type=click.Choice(['aggressive', 'polite']))

def crawl(url,limit, depth,proxies, crawl_mode):
    if(bool(urlparse(url).scheme)):
        pass
    else:
        url = 'http://' + url
    
    if limit is None:
        limit = -1
    if depth is None:
        depth = -1
    
    if crawl_mode == 'aggressive':
        mode = 2
    elif crawl_mode == 'polite':
        mode = 1
    else:
        mode = 0

    if proxies:
        Spider(url,limit,depth,proxy=1,crawl_mode=mode)
    else:
        Spider(url,limit,depth,proxy=0,crawl_mode=mode)

if __name__ == '__main__':
    try:
        crawl()
    except:
        pass