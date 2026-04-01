from cell import Cell
import random

def process_config():
    # in der Konfig werden werte angegeben diese werden mit dieser funktion in einem dictionary gespeichert
    with open("config.txt", "r") as file:
        config = {}
        for line in file:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            key, value = line.split("=", 1)
            if key in ("WIDTH", "HEIGHT", "SEED"):
                value = int(value)
            if key in ("ENTRY", "EXIT"):
                x, y = value.split(",")
                x = int(x)
                y = int(y)
                value = (x, y)
            if key == "PERFECT":
                value = value == "True"
            config[key] = value
    return config


class Mazegenerator:
    def __init__(self, width, height, entry, exitcell, perfect, seed):
        # hier speichern wir die werte aus der config in den entsprechenden attributen der klasse
        self.width = width
        self.height = height
        self.entry = entry
        self.exitcell = exitcell
        self.perfect = perfect
        self.seed = seed
        self.maze = None

    def create_grid(self, config):
        # hier erstellen wir die grid mit zellen basierend auf der width und height aus der config
        x = config["WIDTH"]
        y = config["HEIGHT"]
        arr = [[Cell(i, j) for j in range(y)] for i in range(x)]
        #print(arr)
        self.maze = arr

    def shortest_path(self):
        pass

    def to_hex_rows(self):
        pass

    def validate_config(self, config):
        # wir validieren die von process_config im dictionary config gespeicherten werte
        width = config.get("WIDTH")
        height = config.get("HEIGHT")
        entry = config.get("ENTRY")
        exitcell = config.get("EXIT")
        perfect = config.get("PERFECT")
        seed = config.get("SEED")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("WIDTH must be a positive integer.")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("HEIGHT must be a positive integer.")
        if not (
            isinstance(entry, tuple)
            and len(entry) == 2
            and all(isinstance(coord, int) for coord in entry)
        ):
            raise ValueError("ENTRY must be a tuple of two integers.")
        if not (
            isinstance(exitcell, tuple)
            and len(exitcell) == 2
            and all(isinstance(coord, int) for coord in exitcell)
        ):
            raise ValueError("EXIT must be a tuple of two integers.")
        if not isinstance(perfect, bool):
            raise ValueError("PERFECT must be a boolean value.")
        if not isinstance(seed, int):
            raise ValueError("SEED must be an integer.")

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        x = cell.x
        y = cell.y

        if x > 0 and not self.maze[x - 1][y].visited:  # links
            neighbors.append(self.maze[x - 1][y])
        if x < self.width - 1 and not self.maze[x + 1][y].visited:  # rechts
            neighbors.append(self.maze[x + 1][y])
        if y > 0 and not self.maze[x][y - 1].visited:  # oben
            neighbors.append(self.maze[x][y - 1])
        if y < self.height - 1 and not self.maze[x][y + 1].visited:  # unten
            neighbors.append(self.maze[x][y + 1])

        return neighbors

    def remove_wall(self, current, neighbor):
        # rechts
        if neighbor.x == current.x + 1:
            current.wall &= ~2
            neighbor.wall &= ~8
        # links
        elif neighbor.x == current.x - 1:
            current.wall &= ~8
            neighbor.wall &= ~2
        # unten
        elif neighbor.y == current.y + 1:
            current.wall &= ~4
            neighbor.wall &= ~1
        # oben
        elif neighbor.y == current.y - 1:
            current.wall &= ~1
            neighbor.wall &= ~4

    def generate_maze(self):
        config = process_config()
        self.validate_config(config)
        self.create_grid(config)
        entry_x, entry_y = self.entry
        current = self.maze[entry_x][entry_y]
        current.visited = True
        stack = []
        while True:
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                neighbor = random.choice(neighbors)
                stack.append(current)
                self.remove_wall(current, neighbor)
                current = neighbor
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                break
        
            





if __name__ == "__main__":


# current = self.maze[0][0]
# neighbors = self.get_unvisited_neighbors(current)
# neighbor = irgendeiner aus neighbors
# self.remove_wall(current, neighbor)
