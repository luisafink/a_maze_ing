class Cell:
    """One maze cell with bit-encoded walls."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.wall = 15
        self.visited = False
        self.blocked = False
