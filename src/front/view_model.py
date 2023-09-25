import os.path

from src.backend.loader import *
from src.utils.config import raw_path


class ViewModel:
    def __init__(self):
        name_map = {"rail":"中国铁路"}
        self.keys = ["rail"]
        self.names = ["中国铁路"]
        # name_map = {}
        #
        # paths1= os.path.abspath(os.path.join(os.getcwd(), "./backend/data/raw/name_map"))
        # paths2 = os.path.abspath(os.path.join(os.getcwd(), "./backend/data/raw"))
        #
        # with open(paths1, 'r', encoding='utf8') as f:
        #     for line in f.readlines():
        #         name_map[line.split(':')[0].strip()] = line.split(':')[1].strip()
        # self.keys = []
        # self.names = []
        # for file_name in os.listdir(paths2):
        #     if not os.path.isdir(paths2 + "\\"+file_name):
        #         print(paths2 + file_name)
        #         print(os.path.isdir(paths2 + file_name))
        #         continue
        #     self.keys.append(file_name.strip())
        #     if file_name in name_map.keys():
        #         self.names.append(name_map[file_name])
        #     else:
        #         self.names.append(file_name)

        self.graphs = {}
        self.graph_raw = {}
        self.current_graph = None
        for key in self.keys:
            if key == 'red':
                self.graph_raw[key] = load_red_graph()
                self.graphs[key] = load_red_graph()
            elif key == 'west':
                self.graph_raw[key] = load_west_graph()
                self.graphs[key] = load_west_graph()
            elif key == 'kingdom':
                self.graph_raw[key] = load_kingdom_graph()
                self.graphs[key] = load_kingdom_graph()
            elif key == 'who':
                self.graph_raw[key] = load_who_graph()
                self.graphs[key] = load_who_graph()
            elif key == 'rail':
                self.graph_raw[key] = load_rail_graph()
                self.graphs[key] = load_rail_graph()
            else:
                self.graph_raw[key] = load_any_graph(key)
                self.graphs[key] = load_any_graph(key)

        self.is_ia = False
        self.ia_selected = []
        self.ready_upload = False
        self.upload_key = None
        self.upload_content = None

    def add_graph(self, key):
        self.keys.append(key)
        self.names.append(key)
        self.graphs[key] = load_any_graph(key)
        self.graph_raw[key] = load_any_graph(key)

    def get_graph(self, key, reset=False):
        if key not in self.graphs.keys():
            self.add_graph(key)
        if reset:
            if key == 'red':
                self.graphs[key] = load_red_graph()
            elif key == 'west':
                self.graphs[key] = load_west_graph()
            elif key == 'kingdom':
                self.graphs[key] = load_kingdom_graph()
            elif key == 'who':
                self.graphs[key] = load_who_graph()
            elif key == 'rail':
                self.graphs[key] = load_rail_graph()
            else:
                self.graphs[key] = load_any_graph(key)
            self.current_graph = self.graphs[key]
            return self.graph_raw[key]
        else:
            self.current_graph = self.graphs[key]
            return self.graphs[key]


