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
            d = json.load(f)
            self.start_node = d["pickup-point"]
            self.start_direction = d["start-direction"]
            self.points = {}
            points_data = d["points"]
            for (_, key) in enumerate(points_data):
                point = points_data[key]
                self.points[key] = Node(self, key, point)

class Node:
    def __init__(self, maze: Maze, name, point_data):
        self.maze = maze
        self.name = name
        self.x = point_data["x"]
        self.y = point_data["y"]

        self.connected_nodes: dict[Direction, str] = {}
        for _, direction in enumerate(Direction):
            if direction in point_data:
                self.connected_nodes[direction] = point_data[direction]

    def get_connected_node(self, direction: Direction):
        if direction in self.connected_nodes:
            node_id = self.connected_nodes[direction]
            return self.maze.points[node_id]

class Bot:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.current_node: Node = maze.start_node
        self.direction = maze.start_direction
        self.current_orders = []
    
    def next_expected_node(self) -> Node | None:
        return self.current_node.get_connected_node(self.direction)

    def add_order(self, order):
        self.current_orders.append(order)

    def reached_crossing(self):
        next_node = self.next_expected_node()
        if next_node:
            self.current_node = next_node

