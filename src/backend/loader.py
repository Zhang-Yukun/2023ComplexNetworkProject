import os.path
import pickle
import random
import sys
from os import path
import pandas as pd

from src.backend.model.graph import Graph
from src.backend.process import generate_novel_graph

current_path = os.path.dirname(__file__)
print(current_path)
def generate_random_graph(size):
    g = Graph()
    for i in range(size):
        g.add_node("node{}".format(i), "node{}".format(i))
    rdm = random.Random()
    for i in range(size * (size - 1) // 2):
        if rdm.random() > 0.8:
            rf = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
            rt = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
            while rf == rt:
                rf = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
                rt = [i for i in g.id2nodes.keys()][rdm.randint(0, g.size - 1)]
            g.add_edge(rf, rt, rdm.randint(1, 3))
    return g


def load_graph(clz, label):
    sys.setrecursionlimit(3000)
    g = clz()
    if path.exists("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/cache/{}.pkl".format(label)):
        print('load graph {} from disk...'.format(label))
        return pickle.load(open("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/cache/{}.pkl".format(label), 'rb'))
    # if not path.exists('backend/data/parsed/{}/names.txt'.format(label)):
    #     generate_novel_graph(label)
    df = pd.read_csv("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/node.csv")
    for index, row in df.iterrows():
        g.add_node(row["node"], row["node"])
    df = pd.read_csv("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/edge_simple.csv")
    for index, row in df.iterrows():
        g.add_edge(row["start_station_name"], row["end_station_name"], float(row["running_time"]))
    # with open(current_path+ '/data/parsed/{}/names.txt'.format(label), 'r',encoding='utf8') as f:
    #     for x in f.readlines():
    #         g.add_node(x.strip(), x.strip())
    # with open(current_path+'/data/parsed/{}/edges.txt'.format(label), 'r',encoding='utf8') as f:
    #     for ed in f.readlines():
    #         ed = ed.split(";")
    #         n1 = ed[0].strip()
    #         n2 = ed[1].strip()
    #         g.add_edge(n1, n2, float(ed[2].strip()))
    print('calculating properties for {}'.format(label))
    g.calc_dists()
    g.calc_coreness()
    g.calc_cluster_coefficient()
    print('calculation properties for {} done'.format(label))
    if not os.path.exists("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/cache/"):
        os.makedirs("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/cache/")
    pickle.dump(g, open("/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/cache/{}.pkl".format(label), "wb"))
    return g

class RailGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]
def load_rail_graph() -> object:
    return load_graph(RailGraph, "graph")

def load_any_graph(key) -> object:
    return load_graph(Graph, key)
