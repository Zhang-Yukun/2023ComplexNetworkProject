import math
import tqdm
import numpy as np

from src.backend.model.node import Node
from src.utils.color import random_color


class Graph:
    def __init__(self):
        self.size = 0
        self.nodes = set()
        self.node_to_id = {}
        self.id_to_node = {}
        self.edges = {}
        self.distances = {}
        self.diameter = 0
        self.average_degree = 0
        self.average_path_length = 0
        self.cluster_coefficient = {}
        self.coreness = {}
        self.degrees = {}
        self.connected_components_num = None
        self.connected_components_set = {}

    def add_node(self, node: Node):
        self.node_to_id[node] = node.id
        self.id_to_node[node.id] = node
        self.nodes.add(node)
        self.size += 1

    def add_nodes(self, node_list: list[Node]):
        for node in tqdm.tqdm(node_list):
            self.add_node(node)

    def remove_nodes(self, node_ids):
        for index in node_ids:
            node = self.id_to_node[index]
            for neighbour_id in node.get_all_neighbours_id():
                neighbour = self.id_to_node[neighbour_id]
                neighbour.remove_neighbour(index)
            delete_list = [pair for pair in self.edges.keys() if index in pair]
            for pair in delete_list:
                self.edges.pop(pair)
            self.node_to_id.pop(node)
            self.id_to_node.pop(index)
            self.degrees.pop(node)
            self.nodes.remove(node)
            self.size -= 1
        self.calculate_all_properties()

    def add_edge(self, source_id, target_id, weight=0.0):
        if source_id == target_id:
            return
        if (source_id in self.node_to_id.values()
                and target_id in self.node_to_id.values()):
            if ((source_id, target_id) not in self.edges.keys()
                    and (target_id, source_id) not in self.edges.keys()):
                self.edges[(source_id, target_id)] = weight
            self.id_to_node[source_id].neighbours[target_id] = weight
            self.id_to_node[target_id].neighbours[source_id] = weight

    def add_edges(self, edge_list):
        for edge in tqdm.tqdm(edge_list):
            self.add_edge(edge[0], edge[1], edge[2])

    def remove_edges(self, edges):
        for edge in edges:
            self.edges.pop((edge[0], edge[1]))
            source_node = self.id_to_node[edge[0]]
            target_node = self.id_to_node[edge[1]]
            source_node.neighbours.pop(edge[1])
            target_node.neighbours.pop(edge[0])
        self.calculate_all_properties()

    # 基本参数的计算
    def calculate_all_properties(self):
        self.calculate_degree()
        self.calculate_average_degree()
        self.calculate_distances()
        self.calculate_average_path_length()
        self.calculate_diameter()
        self.calculate_connected_components_num()
        self.calculate_cluster_coefficient()
        self.calculate_coreness()

    def calculate_degree(self):
        for node in self.nodes:
            self.degrees[node] = node.get_degree()

    def get_degree(self):
        return self.degrees

    def calculate_average_degree(self):
        self.average_degree = np.average([x for x in self.degrees.values()])

    def get_average_degree(self):
        return self.average_degree

    def calculate_distances(self):
        """
        计算任意两个结点之间的距离
        """
        distances = {}
        # for source in self.nodes:
        #     for target in self.nodes:
        #         distances[(source.id, target.id)] = math.inf
        # for node in self.nodes:
        #     distances[(node.id, node.id)] = 0
        #     for neighbour_id in node.get_all_neighbours_id():
        #         distances[(node.id, neighbour_id)] = node.neighbours[neighbour_id]
        # for k in tqdm.tqdm(self.nodes):
        #     for i in self.nodes:
        #         for j in self.nodes:
        #             if distances[(i.id, j.id)] > distances[(i.id, k.id)] + distances[(k.id, j.id)]:
        #                 distances[(i.id, j.id)] = distances[(i.id, k.id)] + distances[(k.id, j.id)]
        # visited_nodes = set()
        # for node in tqdm.tqdm(self.nodes):
        #     u = []
        #     v = [x.id for x in self.nodes if x not in visited_nodes]
        #     distance = {index: math.inf for index in v}
        #     distance[node.id] = 0
        #     visited_nodes.add(node)
        #     while v:
        #         v = sorted(v, key=lambda x: distance[x])
        #         current = self.id_to_node[v.pop(0)]
        #         u.append(current.id)
        #         for next_id in [x for x in current.get_all_neighbours_id() if self.id_to_node[x] not in visited_nodes]:
        #             if next_id not in u:
        #                 distance[next_id] = min(distance[next_id],
        #                                         distance[current.id] + current.neighbours[next_id])
        #             if (node, current) not in distances.keys():
        #                 distances[(node, current)] = distance[current.id]
        for node in tqdm.tqdm(self.nodes):
            u = []
            v = [x.id for x in self.nodes]
            distance = {index: math.inf for index in v}
            distance[node.id] = 0
            while v:
                v = sorted(v, key=lambda x: distance[x])
                current = self.id_to_node[v.pop(0)]
                u.append(current.id)
                for next_id in current.get_all_neighbours_id():
                    if next_id not in u:
                        distance[next_id] = min(distance[next_id],
                                                distance[current.id] + current.neighbours[next_id])
                    if (node, current) not in distances.keys():
                        distances[(node, current)] = distance[current.id]
        self.distances = distances

    def get_distance(self, x, y):
        xn = self.id_to_node[x]
        yn = self.id_to_node[y]
        if (xn, yn) in self.distances.keys():
            return self.distances[(xn, yn)]
        if (yn, xn) in self.distances.keys():
            return self.distances[(yn, xn)]

    def calculate_average_path_length(self):
        avg = 0
        cnt = 0
        for x, y in self.distances.items():
            if y != math.inf and y != 0:
                cnt += 1
                avg += y
        self.average_path_length = avg / cnt

    def get_average_path_length(self):
        return self.average_path_length

    def calculate_diameter(self):
        diameter = 0
        for x, y in self.distances.items():
            if y != math.inf:
                diameter = max(diameter, y)
        self.diameter = diameter

    def get_diameter(self):
        return self.diameter

    def calculate_connected_components_num(self):
        connected_components_set = {}
        visit = []
        num = 0
        for node in tqdm.tqdm(self.nodes):
            if node.id in visit:
                continue
            connected_components_set[num] = set()
            queue = [node.id]
            while queue:
                current = self.id_to_node[queue.pop(0)]
                connected_components_set[num].add(current)
                for neighbour_id in current.get_all_neighbours_id():
                    if neighbour_id not in visit:
                        visit.append(neighbour_id)
                        queue.append(neighbour_id)
            num += 1
        self.connected_components_set = connected_components_set
        self.connected_components_num = num

    def get_connected_component_set(self):
        return self.connected_components_set

    def get_connected_component_num(self):
        """
        获得连通分量数
        """
        return self.connected_components_num

    def calculate_cluster_coefficient(self):
        """
        计算每个结点的聚类系数
        """
        cluster_coefficient = {}
        for node in tqdm.tqdm(self.nodes):
            degree = node.get_degree()
            if degree < 2:
                cluster_coefficient[node] = 0
            else:
                actual_edge_num = 0
                neighbours = node.get_all_neighbours_id()
                neighbours_len = len(neighbours)
                for i in range(neighbours_len):
                    for j in range(i + 1, neighbours_len):
                        if neighbours[i] in self.id_to_node[neighbours[j]].get_all_neighbours_id():
                            actual_edge_num += 1
                cluster_coefficient[node] = (2.0 * actual_edge_num) / (neighbours_len * (neighbours_len - 1))
        self.cluster_coefficient = cluster_coefficient

    def get_cluster_coefficient(self):
        return np.average([x for x in self.cluster_coefficient.values()])

    def calculate_coreness(self):
        """
        计算coreness
        """
        degrees = {}
        coreness = {}
        for node in self.nodes:
            degrees[node] = node.get_degree()
            coreness[node] = 0
        k = 0
        while degrees:
            min_degree_node = min(degrees, key=degrees.get)
            min_degree = degrees[min_degree_node]
            while k < min_degree:
                k += 1
            coreness[min_degree_node] = k
            for neighbour_id in min_degree_node.get_all_neighbours_id():
                neighbour_node = self.id_to_node[neighbour_id]
                if neighbour_node in degrees.keys():
                    degrees[neighbour_node] -= 1
            degrees.pop(min_degree_node)
        self.coreness = coreness

    def get_coreness(self):
        return max(self.coreness.values())

    def get_degree_distribution(self):
        dis = {}
        for node in self.nodes:
            dis.setdefault(node.get_degree(), 0)
            dis[node.get_degree()] += 1
        return dis

    def get_node_color_map(self):
        class_color_map = {}
        for node in self.nodes:
            # class_color_map[node_class] = "#097AFF"
            # class_color_map[node_class] = random_color(1000)
            class_color_map[node.id] = random_color(len(class_color_map))
        return class_color_map

    def get_popular_nodes(self, n=None):
        nodes = [(n, n.get_degree()) for n in self.nodes]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        if n is None:
            n = len(nodes)
        return nodes[:n]

    def get_low_cluster_nodes(self, n=None):
        nodes = [(n, v) for n, v in self.cluster_coefficient.items()]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=False)
        if n is None:
            n = len(nodes)
        return nodes[:n]

    def get_high_coreness_nodes(self, n=None):
        nodes = [(n, cn) for n, cn in self.coreness.items()]
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        if n is None:
            n = len(nodes)
        return nodes[:n]
