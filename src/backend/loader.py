import os.path
import pickle
import random
import sys
from os import path
import pandas as pd

from src.backend.model.node import Node
from src.backend.model.graph import Graph


def generate_random_graph(size):
    g = Graph()
    for i in range(size):
        g.add_node("node{}".format(i), "node{}".format(i))
    rdm = random.Random()
    for i in range(size * (size - 1) // 2):
        if rdm.random() > 0.8:
            rf = [i for i in g.id_to_node.keys()][rdm.randint(0, g.size - 1)]
            rt = [i for i in g.id_to_node.keys()][rdm.randint(0, g.size - 1)]
            while rf == rt:
                rf = [i for i in g.id_to_node.keys()][rdm.randint(0, g.size - 1)]
                rt = [i for i in g.id_to_node.keys()][rdm.randint(0, g.size - 1)]
            g.add_edge(rf, rt, rdm.randint(1, 3))
    return g


def load_graph(clz, label):
    base_path = "/Applications/LANGUAGE/PYTHON/2023ComplexNetworkProject/data/"
    sys.setrecursionlimit(3000)
    g = clz()
    if path.exists(base_path + "cache/{}.pkl".format(label)):
        print('load graph {} from disk...'.format(label))
        return pickle.load(open(base_path + "/cache/{}.pkl".format(label), 'rb'))
    # if not path.exists('backend/data/parsed/{}/names.txt'.format(label)):
    #     generate_novel_graph(label)
    df = pd.read_csv(base_path + "station_coordinate.csv")
    for index, row in df.iterrows():
        g.add_node(Node(index=row["station"], name=row["station"], longitude=row["longitude"], latitude=row["latitude"]))
    df = pd.read_csv(base_path + "edge_simple.csv")
    for index, row in df.iterrows():
        g.add_edge(row["start_station_name"], row["end_station_name"], float(row["running_time"]))
    print('calculating properties for {}'.format(label))
    g.calculate_distances()
    g.calculate_coreness()
    g.calculate_cluster_coefficient()
    g.calculate_diameter()
    g.calculate_connected_components_num()
    print('calculation properties for {} done'.format(label))
    if not os.path.exists(base_path + "cache/"):
        os.makedirs(base_path + "cache/")
    pickle.dump(g, open(base_path + "cache/{}.pkl".format(label), "wb"))
    return g

class RailGraph(Graph):
    def get_node_class(self, node):
        return node.label[0]
def load_rail_graph() -> object:
    return load_graph(RailGraph, "graph")

def load_any_graph(key) -> object:
    return load_graph(Graph, key)
