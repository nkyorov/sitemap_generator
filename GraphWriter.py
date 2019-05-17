import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urljoin, urlparse
import tldextract
import numpy as np

class GraphWriter:
    def __init__(self,url):
        self.g = nx.Graph()
        self.createGraph(url)
        self.saveGraph()

    def createGraph(self,url):
        for i in range(len(url)):
            parsed= urlparse(url[i])
            print('path    :', parsed.path) 
            print('hostname:', parsed.hostname)

            self.g.add_node(parsed.hostname)
            self.g.add_edge(parsed.hostname,parsed.path)
                
    def saveGraph(self):
        pos = nx.spring_layout(self.g,k=0.3*1/np.sqrt(len(self.g.nodes())))
        nx.draw(self.g, with_labels=True,pos=pos)
        plt.savefig("graph.pdf")
        
        return nx.write_gexf(self.g,"graph.gexf")

