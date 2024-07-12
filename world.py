from enum import Enum

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class Maze:
    def __init__(self):
        self.start_node = Node()

class Node:
    def __init__(self):
        self.connected_nodes: dict[Direction, Node | None] = {
            Direction.NORTH: None,
            Direction.EAST: None,
            Direction.SOUTH: None,
            Direction.WEST: None
        }

    def get_connected_node(self, direction: Direction):
        return self.connected_nodes[direction]

class BotState:
    def __init__(self, maze: Maze) -> None:
        self.current_node: Node = maze.start_node
        self.direction = Direction.NORTH
    
    def next_expected_node(self) -> Node | None:
        node = self.current_node
        node.connected_nodes[self.direction]

    def add_crossing(self):
        new_node = Node()
        self.current_node.connected_nodes[self.direction] = new_node
        self.current_node = new_node

def get_opposite_direction(direction):
    lookup  = {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.EAST: Direction.WEST,
        Direction.WEST: Direction.EAST,
    }
    return lookup[direction]

class World:
    def __init__(self, maze, bot) -> None:
        self.maze = maze
        self.bot = bot
