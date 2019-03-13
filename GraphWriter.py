import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urljoin, urlparse
import tldextract

class GraphWriter:
    def __init__(self,url):
        self.g = nx.Graph()
        self.createGraph(url)
        self.printGraph()

    def createGraph(self,url):
        for i in range(len(url)):
            parsed= urlparse(url[i])
            print('path    :', parsed.path) 
            print('hostname:', parsed.hostname)

            self.g.add_node(parsed.hostname)
            self.g.add_edge(parsed.hostname,parsed.path)
                
    def printGraph(self):
        print(nx.info(self.g))
        nx.draw(self.g, with_labels=True,font_weight='bold')
        return plt.show()


# urls = {'http://quotes.toscrape.com/tag/simile/', 'http://quotes.toscrape.com/random/', 'http://quotes.toscrape.com/tableful/', 'http://quotes.toscrape.com/search.aspx/', 'http://quotes.toscrape.com/js/', 'http://quotes.toscrape.com/scroll/', 'http://quotes.toscrape.com/', 'http://toscrape.com/', 'http://quotes.toscrape.com/login/', 'http://books.toscrape.com/'}
# GraphWriter(list(urls))
