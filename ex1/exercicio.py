import re
from matplotlib import pyplot as plt

import networkx as nx
import numpy as np
import math

class Exercicio():
    def __init__(self, nome_base):
        self.G = nx.read_edgelist(f'data/{nome_base}.txt', nodetype=int, data=(('weight', float),))
        return
    

    def exibir_grafo(self, mostrarLegendas=False):
        plt.figure(figsize=(12,10))
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, node_color='lightgreen', node_size=len(self.G), with_labels=mostrarLegendas)
        return
    

    def distribuicao_grau(self):
        vk = dict(self.G.degree())
        vk = list(vk.values())
        vk = np.array(vk)
        maxk = np.max(vk)
        kvalues = np.arange(0,maxk+1)
        Pk = np.zeros(maxk+1)
        for k in vk:
            Pk[k] = Pk[k] + 1
        Pk = Pk/sum(Pk)
        return kvalues, Pk
    
    
    def momento_grau(self, m):
        return np.sum([(self.G.degree(i)**m)/len(self.G) for i in self.G.nodes])


    def grau_medio(self):
        return np.sum([degree/len(self.G) for _, degree in self.G.degree()])
    

    def coef_complexidade(self):
        return self.momento_grau(2) / self.grau_medio()
    

    def entropia_shannon(self):
        _,Pk = self.distribuicao_grau()
        H = 0
        for p in Pk:
            if(p > 0):
                H -= p * math.log(p, 2)
        return H
    

    def transistividade(self):
        return nx.transitivity(self.G)


    def agrupamento_medio(self):
        return nx.average_clustering(self.G)
    