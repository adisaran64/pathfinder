# Pathfinder - Aditya Saravanan
# A program for finding the shortest path between two different points on a 2-D grid.

class Node:
    """A node, meant to act as a single-unit square on a graph."""
    can_use = True
    distance = float('inf')
    weight = 1
    previous_node = None

    def __init__(self, x_pos, y_pos):
        self.x_coordinate = x_pos
        self.y_coordinate = y_pos
        self.coordinates = [x_pos, y_pos]
        self.connections = []

    def check_node_neighbors(node1, node2):
        if node1.x_coordinate == node2.x_coordinate:
            if abs(node1.y_coordinate - node2.y_coordinate) == 1:
                return True
            return False
        elif node1.y_coordinate == node2.y_coordinate:
            if abs(node1.x_coordinate - node2.x_coordinate) == 1:
                return True
            return False
        return False


class Board:
    """A Board consists of many nodes, bound together to make a graph-like structure."""
    def __init__(self, x_size, y_size):
        self.values = []
        self.fill_board(x_size, y_size)
        self.make_connections()

    def fill_board(self, x_size, y_size):
        for xcounter in range(x_size+1):
            for ycounter in range(y_size+1):
                self.values.append(Node(xcounter, ycounter))

    def make_connections(self):
        for node in self.values:
            for other_node in self.values:
                if Node.check_node_neighbors(node, other_node):
                    node.connections.append(other_node)

    def find_node_from_coordinates(self, point):
        for node in self.values:
            if node.coordinates == point:
                return node
        raise ValueError("Those coordinates do not correspond to a node on the board!")
