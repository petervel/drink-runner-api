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
        with open(filename) as file:
            d = json.load(file)
            self.start_node = d["pickup-point"]
            self.start_direction = d["start-direction"]
            self.points = {}
            points_data = d["points"]
            for (_, key) in enumerate(points_data):
                point = points_data[key]
                self.points[key] = Node(self, key, point)
            print("maze loaded.")

class Node:
    def __init__(self, maze: Maze, name, point_data):
        self.maze = maze
        self.name = name
        self.x = point_data["x"]
        self.y = point_data["y"]

        self.connected_nodes: dict[Direction, str] = {}
        for direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
            if direction.value in point_data:
                self.connected_nodes[direction] = point_data[direction.value]

    def get_connected_node(self, direction: Direction):
        if direction in self.connected_nodes:
            node_id = self.connected_nodes[direction]
            return self.maze.points[node_id]

class Order:
    def __init__(self, point_id, count):
        self.point_id = point_id
        self.count = count
class Bot:
    def __init__(self, maze: Maze, filename: str) -> None:
        self.maze = maze
        self.current_node: Node = maze.points[maze.start_node]
        if maze.start_direction == "north":
            maze.start_direction = Direction.NORTH
        elif maze.start_direction == "east":
            maze.start_direction = Direction.EAST
        elif maze.start_direction == "south":
            maze.start_direction = Direction.SOUTH
        else:
            maze.start_direction = Direction.WEST
            
        self.direction = maze.start_direction
        self.current_orders = []
        with open(filename) as file:
            orders = json.load(file)
            for order in orders:
                self.add_order(Order(order["point"], order["count"]))
        
    def next_expected_node(self) -> Node | None:
        return self.current_node.get_connected_node(self.direction)

    def add_order(self, order):
        print(f"Adding order {order}")
        self.current_orders.append(order)

    def reached_crossing(self):
        next_node = self.next_expected_node()
        print(f"{self.direction}...{self.current_node.connected_nodes}")
        if next_node:
            print(f"Moving from {self.current_node.name} to {next_node.name}")
            self.current_node = next_node
            
        print(f"Current node: {self.current_node.name}")

    def turned_left(self):
        lookup = {
            Direction.EAST: Direction.NORTH,
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST
        }
        self.direction = lookup[self.direction]
        
    def turned_right(self):
        lookup = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH
        }
        self.direction = lookup[self.direction]
    
    # TODO
    def get_target(self):
        return "e"
    
    def get_shortest_route_to(self, start_node, target_id):
        pass
        # best_route = None
        # for connected_node_id in self.current_node.connected_nodes.values():
            
            
    
    def get_next_instruction(self):
        pass
        # target_id = self.get_target()
        # route = self.get_shortest_route(self.current_node, target_id)
        # return route[0]
        
        