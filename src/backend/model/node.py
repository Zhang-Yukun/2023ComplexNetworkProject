
class Node:
    def __init__(self, index, name, city="", longitude=0.0, latitude=0.0):
        self.id = index
        self.name = name
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.neighbours = {}
        # self.next_neighbours = {}
        # self.previous_neighbours = {}

    # def get_next_neighbours_id(self):
    #     return list(self.next_neighbours.keys())
    #
    # def get_previous_neighbours_id(self):
    #     return list(self.previous_neighbours.keys())

    def get_all_neighbours_id(self):
        # return list(self.next_neighbours.keys()) + list(self.previous_neighbours.keys())
        return list(self.neighbours.keys())

    def remove_neighbour(self, neighbour_id):
        if neighbour_id in self.neighbours.keys():
            self.neighbours.pop(neighbour_id)
        # if neighbour_id in self.next_neighbours.keys():
        #     del self.next_neighbours[neighbour_id]
        # if neighbour_id in self.previous_neighbours.keys():
        #     del self.previous_neighbours[neighbour_id]

    def get_degree(self):
        # return len(self.next_neighbours) + len(self.previous_neighbours)
        return len(self.neighbours)

    # def get_degree_in(self):
    #     return len(self.previous_neighbours)
    #
    # def get_degree_out(self):
    #     return len(self.next_neighbours)

# class Node:
#     def __init__(self, graph, id,  lat, lng, label=""):
#         self.graph = graph
#         self.label = label
#         self.id = id
#         self.lat = lat
#         self.lng = lng
#         self.neighbours = {}
#         self.prevs = {}
#
#     def get_all_neighbour_id(self):
#         return list(self.neighbours.keys()) + list(self.prevs.keys())
#
#     def remove_neighbour(self, nb_id):
#         if nb_id in self.neighbours.keys():
#             del self.neighbours[nb_id]
#         if nb_id in self.prevs.keys():
#             del self.prevs[nb_id]
#
#     def get_degree(self):
#         return len(self.neighbours) + len(self.prevs)
#
#     def get_degree_in(self):
#         return len(self.prevs)
#
#     def get_degree_out(self):
#         return len(self.neighbours)
