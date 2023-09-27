
class Node:
    def __init__(self, index, name, city="", longitude=0.0, latitude=0.0):
        self.id = index
        self.name = name
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.neighbours = {}

    def get_all_neighbours_id(self):
        return list(self.neighbours.keys())

    def remove_neighbour(self, neighbour_id):
        if neighbour_id in self.neighbours.keys():
            self.neighbours.pop(neighbour_id)

    def get_degree(self):
        return len(self.neighbours)
