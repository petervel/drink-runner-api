    from enum import Enum
    import json
    import heapq

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
        
    def next_expected_node(self) -> Node | None:
        return self.current_node.get_connected_node(self.direction)

    def add_order(self, order):
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
        
        def get_shortest_route_to(self, start_node: Node, target_id: str):
            # Initialize the priority queue with the start node
            queue = [(0, start_node)]
            visited = set()
            came_from = {start_node.name: None}
            cost_so_far = {start_node.name: 0}
            
            while queue:
                current_cost, current_node = heapq.heappop(queue)
                
                # If the target is reached, reconstruct the path
                if current_node.name == target_id:
                    path = []
                    while current_node is not None:
                        path.append(current_node.name)
                        current_node = came_from[current_node.name]
                    path.reverse()
                    return path
                
                visited.add(current_node.name)
                
                # Explore the connected nodes
                for _, neighbor_id in current_node.connected_nodes.items():
                    neighbor = self.maze.points[neighbor_id]
                    new_cost = current_cost + 1  # Assuming the cost to each neighbor is 1
                    if neighbor_id not in cost_so_far or new_cost < cost_so_far[neighbor_id]:
                        cost_so_far[neighbor_id] = new_cost
                        priority = new_cost
                        heapq.heappush(queue, (priority, neighbor))
                        came_from[neighbor_id] = current_node
            
            raise LookupError("DijkstraError: no path found")

                
        def get_next_instruction(self):
            target_id = self.get_target()
            route = self.get_shortest_route_to(self.current_node, target_id)
            return route[0]

    if __name__ == "__main__":
            main()