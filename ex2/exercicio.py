from statistics import mean, variance
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import math

class Exercicio():
    def __init__(self, nome_base):
        self.G = nx.read_edgelist(f'data/{nome_base}.txt', nodetype=int, data=(('weight', float),))
        self.G = self.G.to_undirected()
        self.G.remove_edges_from(nx.selfloop_edges(self.G))
        Gcc = sorted(nx.connected_components(self.G), key=len, reverse=True)
        self.G = self.G.subgraph(Gcc[0])
        self.G = nx.convert_node_labels_to_integers(self.G, first_label=0)
        return
    
    def exibir_grafo(self, mostrarLegendas=False):
        plt.figure(figsize=(12,10))
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, node_color='lightgreen', node_size=len(self.G), with_labels=mostrarLegendas)
        return
    
    def diametro(self):
        return nx.diameter(self.G)
    
    def media_menor_caminho(self):
        return nx.average_shortest_path_length(self.G)

    def variancia_menor_caminho(self):
        return variance(self.distancias())
    
    def coef_assertividade(self):
        return nx.degree_assortativity_coefficient(self.G)


    def entropia_shannon(self):
        _,Pk = self.distribuicao_grau()
        H = 0
        for p in Pk:
            if(p > 0):
                H -= p * math.log(p, 2)
        return H
    

    def distribuicao_grau(self):
        vk = np.array(self.distancias())
        maxk = np.max(vk)
        kvalues = np.arange(0,maxk+1)
        Pk = np.zeros(maxk+1)
        for k in vk:
            Pk[k] = Pk[k] + 1
        Pk = Pk/sum(Pk)
        return kvalues, Pk
    

    def distancias(self):
        N = len(self.G)
        vl = []
        for i in np.arange(0, N):
            for j in np.arange(i+1, N):
                if(i != j):
                    aux = nx.shortest_path(self.G,i,j)
                    vl.append(len(aux)-1)
        return vl

    def corr_Pearson(self):
        knn = []
        for i in self.G.nodes():
            aux =  nx.average_neighbor_degree(self.G, nodes = [i])
            knn.append(float(aux[i]))
        knn = np.array(knn)
        vk = dict(self.G.degree())
        vk = list(vk.values())
        knnk = list()
        ks = list()
        for k in np.arange(np.min(vk), np.max(vk)+1):
            aux = vk == k
            if(len(knn[aux]) > 0):
                av_knn = mean(knn[aux])
                knnk.append(av_knn)
                ks.append(k)
        return np.corrcoef(ks, knnk)[0,1]