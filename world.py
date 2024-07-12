from enum import Enum
import json

class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

class Maze:
    def __init__(self, filename):
        print("loading maze")
        with open(filename) as f:
            print(filename)
            d = json.load(f)
            self.start_node = d["pickup-point"]
            self.start_direction = d["start-direction"]
            nodes_dict = {}
            points_data = d["points"]
            for (_, key) in enumerate(points_data):
                point = points_data[key]
                nodes_dict[key] = Node(key, point)
            
class Node:
    def __init__(self, name, point_data):
        self.name = name
        self.x = point_data["x"]
        self.y = point_data["y"]

        self.connected_nodes: dict[Direction, Node | None] = {}
        for _, direction in enumerate(Direction):
            if direction in point_data:
                self.connected_nodes[direction] = point_data[direction]

    def get_connected_node(self, direction: Direction):
        return self.connected_nodes[direction]

class Bot:
    def __init__(self, maze: Maze) -> None:
        self.current_node: Node = maze.start_node
        self.direction = Direction.NORTH
    
    def next_expected_node(self) -> Node | None:
        node = self.current_node
        node.connected_nodes[self.direction]

    # def add_crossing(self):
    #     new_node = Node()
    #     self.current_node.connected_nodes[self.direction] = new_node
    #     self.current_node = new_node

def get_opposite_direction(direction):
    lookup  = {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.EAST: Direction.WEST,
        Direction.WEST: Direction.EAST,
    }
    return lookup[direction]

