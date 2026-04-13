import tkinter as tk


# ist die wand da oder nicht?
def is_connected(cell1, cell2, connections) -> bool:
    return (cell1, cell2) in connections or (cell2, cell1) in connections


def draw_cell(canvas, row: int, col: int, tile_size: int,
              connections, entry_cell, exit_cell) -> None:
    x1 = col * tile_size  # oben
    y1 = row * tile_size  # links
    x2 = x1 + tile_size  # unten
    y2 = y1 + tile_size  # rechts
    # legt die koordinaten fest nach pixel

    if (row, col) == entry_cell:
        color = "green"  # entry
    elif (row, col) == exit_cell:
        color = "red"  # exit
    else:
        color = "white"  # weg

    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    # oben
    if (row, col) != entry_cell:
        if not is_connected((row, col), (row - 1, col), connections):
            canvas.create_line(x1, y1, x2, y1, width=4)

    # rechts
    if not is_connected((row, col), (row, col + 1), connections):
        canvas.create_line(x2, y1, x2, y2, width=4)

    # unten
    if (row, col) != exit_cell:
        if not is_connected((row, col), (row + 1, col), connections):
            canvas.create_line(x1, y2, x2, y2, width=4)

    # links
    if not is_connected((row, col), (row, col - 1), connections):
        canvas.create_line(x1, y1, x1, y2, width=4)


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
    entry_cell = (0, 1)
    exit_cell = (4, 3)

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            draw_cell(canvas, row, col, tile_size,
                      connections, entry_cell, exit_cell,)  # trailing comma

    root.mainloop()  # Hält das Fenster offen


if __name__ == "__main__":
    start_window()
