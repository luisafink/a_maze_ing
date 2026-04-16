import tkinter as tk


# ist die wand da oder nicht?
# true wenn weg frei
def is_connected(cell1, cell2, connections) -> bool:
    return (cell1, cell2) in connections or (cell2, cell1) in connections


def get_neighbors(cell: tuple[int, int],
                  connections: list[tuple[tuple[int, int], tuple[int, int]]]
                  ) -> list[tuple[int, int]]:
    neighbors: list[tuple[int, int]] = []
    row, col = cell

    possible_neighbors = [
        (row - 1, col),
        (row, col + 1),
        (row + 1, col),
        (row, col - 1),
    ]

    for neighbor in possible_neighbors:
        if is_connected(cell, neighbor, connections):
            neighbors.append(neighbor)
    return neighbors


def find_path(
    entry_cell: tuple[int, int],
    exit_cell: tuple[int, int],
    connections: list[tuple[tuple[int, int], tuple[int, int]]]
        ) -> list[tuple[int, int]]:
    queue: list[tuple[int, int]] = [entry_cell]
    visited: set[tuple[int, int]] = {entry_cell}
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    while queue:
        current = queue.pop(0)  # nimmt erste zahl und "loescht" sie

        if current == exit_cell:
            path = [current]
            # while sucht vom ende bis zum start
            # ist current im path drin dann ist das der weg
            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()  # dreht die reihenfolge um
            return path

        neighbors = get_neighbors(current, connections)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    return []  # wenns kein weg gibt


def draw_cell(canvas, row: int, col: int, tile_size: int,
              connections, entry_cell, exit_cell, path,
              show_path, wall_color) -> None:
    x1 = col * tile_size  # oben
    y1 = row * tile_size  # links
    x2 = x1 + tile_size  # unten
    y2 = y1 + tile_size  # rechts
    # legt die koordinaten fest nach pixel

    if (row, col) == entry_cell:
        color = "green"  # entry
    elif (row, col) == exit_cell:
        color = "red"  # exit
    elif show_path and (row, col) in path:
        color = "lightblue"  # weg wenn er angezeigt werden soll
    else:
        color = "white"  # waende

    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    # oben
    if (row, col) != entry_cell:
        if not is_connected((row, col), (row - 1, col), connections):
            canvas.create_line(x1, y1, x2, y1, width=4, fill=wall_color)

    # rechts
    if not is_connected((row, col), (row, col + 1), connections):
        canvas.create_line(x2, y1, x2, y2, width=4, fill=wall_color)

    # unten
    if (row, col) != exit_cell:
        if not is_connected((row, col), (row + 1, col), connections):
            canvas.create_line(x1, y2, x2, y2, width=4, fill=wall_color)

    # links
    if not is_connected((row, col), (row, col - 1), connections):
        canvas.create_line(x1, y1, x1, y2, width=4, fill=wall_color)


def redraw_maze(canvas, maze, tile_size, connections,
                entry_cell, exit_cell, path, show_path, wall_color,) -> None:
    canvas.delete("all")  # loescht alles was gemalt wurde

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            draw_cell(canvas, row, col, tile_size, connections,
                      entry_cell, exit_cell, path, show_path, wall_color,)
            # malt alles neu
            # es ueberschneidet sich nix und wird frisch gemalt


def start_window() -> None:
    root = tk.Tk()  # Erstellt das Hauptfenster
    root.title("A-Maze-ing")  # Titel oben im Fenster
    root.geometry("800x600")  # Größe des Fensters(root)

    canvas = tk.Canvas(root, width=800, height=600)
    # erstellt malflaeche(flaeche im fenster(root))

    canvas.pack()  # ohne pack wirds oft nicht angezeigt

    tile_size = 80  # groesse der pixel

    maze = [
        [1]*10,
        [1]+[0]*8+[1],
        [1]+[0, 1, 0, 0, 1, 0, 0, 1]+[1],
        [1]+[0]*8+[1],
        [1]*10,
    ]
    connections = [
        ((0, 1), (1, 1)),
        ((1, 1), (1, 2)),
        ((1, 2), (2, 2)),
        ((2, 2), (2, 3)),
        ((2, 3), (3, 3)),
        ((3, 3), (4, 3)),
    ]

    show_path = True

    wall_color = "black"

    entry_cell = (0, 1)
    exit_cell = (4, 3)

    path = find_path(entry_cell, exit_cell, connections)

    redraw_maze(canvas, maze, tile_size, connections,
                entry_cell, exit_cell, path, show_path, wall_color,)
    # trailing comma
    # tkinter hat automatisch event
    # muss einfach dabei sein

    def toggle_path(event) -> None:
        nonlocal show_path  # erkennt variable von ausserhalb
        show_path = not show_path  # true -> false, false -> true

        redraw_maze(canvas, maze, tile_size, connections,
                    entry_cell, exit_cell, path, show_path, wall_color,)

    def change_wall_color(event) -> None:
        nonlocal wall_color

        if wall_color == "black":
            wall_color = "blue"
        elif wall_color == "blue":
            wall_color = "red"
        else:
            wall_color = "black"

        redraw_maze(canvas, maze, tile_size, connections,
                    entry_cell, exit_cell, path, show_path, wall_color,)

    root.bind("p", toggle_path)
    # bind verbindet ereignisse mit funktion
    # taste p = (not) show_path

    root.bind("c", change_wall_color)

    root.mainloop()
    # Hält das Fenster offen
    # alles wird vorbereitet erst dann fenster offen


if __name__ == "__main__":
    start_window()
