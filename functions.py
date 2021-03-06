# Pathfinder - Aditya Saravanan
# A program for finding the shortest path between two different points on a 2-D grid.

from classes import *
import random


### Helper Functions ###

def backtrack_path_creator(final_node):
    """Takes in the final node after performing a pathfinding algorithm,
    backtracks through the "previous_node" attribute to find the shortest path."""
    current_node = final_node
    path_reversed = []
    while current_node is not None:
        path_reversed.append(current_node.coordinates)
        current_node = current_node.previous_node
    return list(reversed(path_reversed))

def random_wall_creator(x_size, y_size):
    """Used to make random walls for the board. Makes it so (approximately) 1/4
    of the board is comprised of walls. Walls created in this function may not be
    unique, but each wall only counts once."""
    walls = []
    while len(walls) < ((x_size + 1) * (y_size + 1)) // 4:
        walls.append([random.randint(0, x_size), random.randint(0, y_size)])
    return walls


### Heuristics ###

def manhattan_distance(start_node, end_node):
    """A popular heuristic for use with the A* algorithm."""
    return (abs(start_node.x_coordinate - end_node.x_coordinate)
            + abs(start_node.y_coordinate - end_node.y_coordinate))


### Algorithms ###

def breadth_first_search(board, start_point, end_point):
    """Performs the breadth-first-search (BFS) pathfinding algorithm."""
    start_node = board.find_node_from_coordinates(start_point)
    queue = []
    visited = []
    queue.append((start_node, [start_point]))
    visited.append(start_node)
    while queue:
        current_node, path_so_far = queue.pop(0)
        for next_node in current_node.connections:
            if next_node not in visited:
                visited.append(next_node)
                if next_node.coordinates == end_point:
                    return path_so_far + [end_point]
                else:
                    queue.append((next_node, path_so_far + [next_node.coordinates]))

def depth_first_search(board, start_point, end_point):
    """Performs the depth-first-search (DFS) pathfinding algorithm."""
    start_node = board.find_node_from_coordinates(start_point)

    def dfs_helper(visited, current_node, path_so_far):
        if current_node.coordinates == end_point:
            return path_so_far
        else:
            for next_node in current_node.connections:
                if next_node not in visited:
                    visited.append(next_node)
                    return dfs_helper(visited, next_node, path_so_far + [next_node.coordinates])

    return dfs_helper([start_node], start_node, [start_point])

def dijkstras(board, start_point, end_point):
    """Performs Dijkstra's pathfinding algorithm."""
    start_node = board.find_node_from_coordinates(start_point)
    for node in board.values:
        node.distance = float('inf')
    start_node.distance = 0
    queue = list(board.values)
    while queue:
        minimum_distance_node = min(queue, key = lambda node: node.distance)
        queue.remove(minimum_distance_node)
        if minimum_distance_node.coordinates == end_point:
            return backtrack_path_creator(minimum_distance_node)
        for next_node in minimum_distance_node.connections:
            if next_node in queue:
                temp = minimum_distance_node.distance + next_node.weight
                if temp < next_node.distance:
                    next_node.distance = temp
                    next_node.previous_node = minimum_distance_node

def a_star(board, start_point, end_point, heuristic=manhattan_distance):
    """Performs the A* pathfinding algorithm, with a heuristic of choice."""
    first_node = board.find_node_from_coordinates(start_point)
    end_node = board.find_node_from_coordinates(end_point)
    for node in board.values:
        node.distance = float('inf')
    first_node.distance = 0 + heuristic(first_node, end_node)
    queue = [first_node]
    while queue:
        minimum_distance_node = min(queue, key = lambda node: node.distance)
        queue.remove(minimum_distance_node)
        if minimum_distance_node.coordinates == end_point:
            return backtrack_path_creator(minimum_distance_node)
        for next_node in minimum_distance_node.connections:
            temp = minimum_distance_node.distance + heuristic(next_node, end_node) + next_node.weight
            if temp < next_node.distance:
                next_node.distance = temp
                next_node.previous_node = minimum_distance_node
                queue.append(next_node)
