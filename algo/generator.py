from __future__ import annotations

from collections import deque
from pathlib import Path
import random
from typing import Deque

from algo.cell import Cell

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

DIRECTIONS = {
    "N": (0, -1, NORTH, SOUTH),
    "E": (1, 0, EAST, WEST),
    "S": (0, 1, SOUTH, NORTH),
    "W": (-1, 0, WEST, EAST),
}

Coord = tuple[int, int]


class MazeGenerator:
    """Generate a maze and export it in the required hex format."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord,
        exit_cell: Coord,
        output_file: str,
        perfect: bool = True,
        seed: int = 0,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_cell = exit_cell
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.rng = random.Random(seed)
        self.maze: list[list[Cell]] = []
        self.pattern_cells: set[Coord] = set()

    @classmethod
    def from_config_file(cls, filename: str) -> "MazeGenerator":
        """Create a generator from a KEY=VALUE config file."""
        values = cls._read_config(filename)

        required = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        }

        missing = required - values.keys()
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"Missing config key(s): {names}")

        width = cls._parse_positive_int(values["WIDTH"], "WIDTH")
        height = cls._parse_positive_int(values["HEIGHT"], "HEIGHT")
        entry = cls._parse_coord(values["ENTRY"], "ENTRY")
        exit_cell = cls._parse_coord(values["EXIT"], "EXIT")
        perfect = cls._parse_bool(values["PERFECT"], "PERFECT")
        output_file = values["OUTPUT_FILE"]
        seed = int(values.get("SEED", "0"))

        generator = cls(
            width,
            height,
            entry,
            exit_cell,
            output_file,
            perfect,
            seed,
        )
        generator.validate_config()
        return generator

    @staticmethod
    def _read_config(filename: str) -> dict[str, str]:
        """Read raw config values from a file."""
        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {filename}")

        values: dict[str, str] = {}

        with path.open("r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(
                        f"Bad config syntax on line {line_number}: {line}"
                    )

                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()

        return values

    @staticmethod
    def _parse_positive_int(value: str, name: str) -> int:
        """Parse a positive integer config value."""
        try:
            number = int(value)
        except ValueError as exc:
            raise ValueError(f"{name} must be an integer") from exc

        if number <= 0:
            raise ValueError(f"{name} must be positive")

        return number

    @staticmethod
    def _parse_coord(value: str, name: str) -> Coord:
        """Parse x,y coordinates."""
        try:
            x_text, y_text = value.split(",", 1)
            return int(x_text), int(y_text)
        except ValueError as exc:
            raise ValueError(f"{name} must look like x,y") from exc

    @staticmethod
    def _parse_bool(value: str, name: str) -> bool:
        """Parse True/False config values."""
        if value == "True":
            return True
        if value == "False":
            return False

        raise ValueError(f"{name} must be True or False")

    def validate_config(self) -> None:
        """Validate values that depend on the maze size."""
        if not self._inside(self.entry):
            raise ValueError("ENTRY must be inside the maze")

        if not self._inside(self.exit_cell):
            raise ValueError("EXIT must be inside the maze")

        if self.entry == self.exit_cell:
            raise ValueError("ENTRY and EXIT must be different")

        if not self.output_file:
            raise ValueError("OUTPUT_FILE must not be empty")

    def generate(self) -> None:
        """Generate a new maze."""
        self.rng = random.Random(self.seed)
        self._create_grid()
        self._place_42_pattern()
        self._carve_with_backtracker()
        self._check_wall_coherence()
        self._check_no_3x3_open_area()

        if self.perfect:
            self._check_perfect_maze()

    def _create_grid(self) -> None:
        """Create a grid where every cell starts fully closed."""
        self.maze = [
            [Cell(x, y) for y in range(self.height)]
            for x in range(self.width)
        ]

    def _place_42_pattern(self) -> None:
        """Place the 42 pattern as fully closed cells."""
        pattern = [
            "X.X.XXX",
            "X.X...X",
            "XXX.XXX",
            "..X.X..",
            "..X.XXX",
        ]

        pattern_width = len(pattern[0])
        pattern_height = len(pattern)

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Warning: maze too small for the 42 pattern; skipped.")
            return

        for top in range(1, self.height - pattern_height):
            for left in range(1, self.width - pattern_width):
                cells = self._pattern_cells_at(pattern, left, top)

                if self.entry in cells or self.exit_cell in cells:
                    continue

                if self._open_grid_is_connected(cells):
                    self.pattern_cells = cells

                    for x, y in cells:
                        self.maze[x][y].blocked = True
                        self.maze[x][y].visited = True

                    return

        print("Warning: could not place the 42 pattern safely; skipped.")

    @staticmethod
    def _pattern_cells_at(
        pattern: list[str],
        left: int,
        top: int,
    ) -> set[Coord]:
        """Return coordinates of all X cells in the pattern."""
        cells: set[Coord] = set()

        for dy, row in enumerate(pattern):
            for dx, char in enumerate(row):
                if char == "X":
                    cells.add((left + dx, top + dy))

        return cells

    def _open_grid_is_connected(self, blocked: set[Coord]) -> bool:
        """Check if all non-blocked cells are connected."""
        start: Coord | None = None

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in blocked:
                    start = (x, y)
                    break
            if start is not None:
                break

        if start is None:
            return False

        seen = {start}
        queue: Deque[Coord] = deque([start])

        while queue:
            x, y = queue.popleft()

            for dx, dy, _, _ in DIRECTIONS.values():
                next_cell = (x + dx, y + dy)

                if not self._inside(next_cell):
                    continue

                if next_cell in blocked or next_cell in seen:
                    continue

                seen.add(next_cell)
                queue.append(next_cell)

        open_cells = self.width * self.height - len(blocked)
        return len(seen) == open_cells

    def _carve_with_backtracker(self) -> None:
        """Carve passages with DFS / recursive backtracker."""
        entry_x, entry_y = self.entry
        current = self.maze[entry_x][entry_y]
        current.visited = True

        stack: list[Cell] = []

        while True:
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                neighbor = self.rng.choice(neighbors)
                stack.append(current)
                self.remove_wall(current, neighbor)
                current = neighbor
                current.visited = True

            elif stack:
                current = stack.pop()

            else:
                break

        for column in self.maze:
            for cell in column:
                if not cell.visited and not cell.blocked:
                    raise ValueError("Maze generation failed: isolated cell")

    def get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        """Return all unvisited direct neighbors."""
        neighbors: list[Cell] = []

        for dx, dy, _, _ in DIRECTIONS.values():
            x = cell.x + dx
            y = cell.y + dy

            if not self._inside((x, y)):
                continue

            neighbor = self.maze[x][y]

            if not neighbor.visited and not neighbor.blocked:
                neighbors.append(neighbor)

        return neighbors

    def remove_wall(self, current: Cell, neighbor: Cell) -> None:
        """Remove the wall between two neighboring cells."""
        dx = neighbor.x - current.x
        dy = neighbor.y - current.y

        for _, (move_x, move_y, wall, opposite_wall) in DIRECTIONS.items():
            if (dx, dy) == (move_x, move_y):
                current.wall &= ~wall
                neighbor.wall &= ~opposite_wall
                return

        raise ValueError("Cells are not direct neighbors")

    def shortest_path(self) -> str:
        """Return the shortest path from entry to exit."""
        queue: Deque[Coord] = deque([self.entry])
        previous: dict[Coord, tuple[Coord, str]] = {}
        seen = {self.entry}

        while queue:
            current = queue.popleft()

            if current == self.exit_cell:
                return self._rebuild_path(previous)

            x, y = current
            cell = self.maze[x][y]

            for letter, (dx, dy, wall, _) in DIRECTIONS.items():
                if cell.wall & wall:
                    continue

                next_cell = (x + dx, y + dy)

                if not self._inside(next_cell):
                    continue

                nx, ny = next_cell

                if self.maze[nx][ny].blocked or next_cell in seen:
                    continue

                seen.add(next_cell)
                previous[next_cell] = (current, letter)
                queue.append(next_cell)

        raise ValueError("No path found from ENTRY to EXIT")

    def _rebuild_path(
        self,
        previous: dict[Coord, tuple[Coord, str]],
    ) -> str:
        """Rebuild path after BFS reached the exit."""
        steps: list[str] = []
        current = self.exit_cell

        while current != self.entry:
            current, letter = previous[current]
            steps.append(letter)

        steps.reverse()
        return "".join(steps)

    def to_hex_rows(self) -> list[str]:
        """Convert maze wall data to hex rows."""
        rows: list[str] = []

        for y in range(self.height):
            row = ""

            for x in range(self.width):
                row += format(self.maze[x][y].wall, "X")

            rows.append(row)

        return rows

    def write_output(self) -> None:
        """Write maze, entry, exit and path to output file."""
        rows = self.to_hex_rows()
        path = self.shortest_path()

        with Path(self.output_file).open("w", encoding="utf-8") as file:
            for row in rows:
                file.write(row + "\n")

            file.write("\n")
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit_cell[0]},{self.exit_cell[1]}\n")
            file.write(path + "\n")

    def render_ascii(self, show_path: bool = False) -> str:
        """Return a simple terminal rendering of the maze."""
        path_cells = self._path_cells() if show_path else set()
        lines: list[str] = []

        lines.append("+" + "---+" * self.width)

        for y in range(self.height):
            middle = "|"
            bottom = "+"

            for x in range(self.width):
                cell = self.maze[x][y]
                coord = (x, y)

                if coord == self.entry:
                    body = " E "
                elif coord == self.exit_cell:
                    body = " X "
                elif coord in self.pattern_cells:
                    body = "###"
                elif coord in path_cells:
                    body = " . "
                else:
                    body = "   "

                east_wall = "|" if cell.wall & EAST else " "
                south_wall = "---" if cell.wall & SOUTH else "   "

                middle += body + east_wall
                bottom += south_wall + "+"

            lines.append(middle)
            lines.append(bottom)

        return "\n".join(lines)

    def _path_cells(self) -> set[Coord]:
        """Return all cells touched by the shortest path."""
        cells = {self.entry}
        x, y = self.entry

        for letter in self.shortest_path():
            dx, dy, _, _ = DIRECTIONS[letter]
            x += dx
            y += dy
            cells.add((x, y))

        return cells

    def _inside(self, coord: Coord) -> bool:
        """Return True if coordinates are inside the maze."""
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def _check_wall_coherence(self) -> None:
        """Ensure neighboring cells agree about shared walls."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[x][y]

                if x + 1 < self.width:
                    right = self.maze[x + 1][y]

                    if bool(cell.wall & EAST) != bool(right.wall & WEST):
                        raise ValueError("Incoherent east/west wall data")

                if y + 1 < self.height:
                    below = self.maze[x][y + 1]

                    if bool(cell.wall & SOUTH) != bool(below.wall & NORTH):
                        raise ValueError("Incoherent north/south wall data")

    def _check_no_3x3_open_area(self) -> None:
        """Reject fully open 3x3 areas."""
        for top in range(self.height - 2):
            for left in range(self.width - 2):
                if self._is_open_3x3(left, top):
                    raise ValueError("Forbidden 3x3 open area found")

    def _is_open_3x3(self, left: int, top: int) -> bool:
        """Return True if a 3x3 area has no internal walls."""
        for y in range(top, top + 3):
            for x in range(left, left + 2):
                if self.maze[x][y].wall & EAST:
                    return False

        for y in range(top, top + 2):
            for x in range(left, left + 3):
                if self.maze[x][y].wall & SOUTH:
                    return False

        return True

    def _check_perfect_maze(self) -> None:
        """Check that the non-blocked maze is a tree."""
        open_cells = 0
        open_edges = 0

        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[x][y]

                if cell.blocked:
                    continue

                open_cells += 1

                if x + 1 < self.width:
                    right = self.maze[x + 1][y]

                    if not right.blocked and not cell.wall & EAST:
                        open_edges += 1

                if y + 1 < self.height:
                    below = self.maze[x][y + 1]

                    if not below.blocked and not cell.wall & SOUTH:
                        open_edges += 1

        if open_edges != open_cells - 1:
            raise ValueError("PERFECT=True failed: maze is not a tree")