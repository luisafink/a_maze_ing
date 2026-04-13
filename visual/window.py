import tkinter as tk


# ist die wand da oder nicht?
def is_connected(cell1, cell2, connections) -> bool:
    return (cell1, cell2) in connections or (cell2, cell1) in connections


def start_window() -> None:
    root = tk.Tk()  # Erstellt das Hauptfenster

    root.title("A-Maze-ing")  # Titel oben im Fenster
    root.geometry("800x600")  # Größe des Fensters

    canvas = tk.Canvas(root, width=800, height=600)  # erstellt malflaeche
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
        ((1, 1), (1, 2)),
        ((1, 2), (2, 2)),
    ]

    entry_cell = (0, 1)
    exit_cell = (4, 3)

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x1 = col * tile_size
            y1 = row * tile_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size
            # verschiebt jedes kaestchen an richtige stelle

            if (row, col) == entry_cell:
                color = "green"   # Entry
            elif (row, col) == exit_cell:
                color = "red"     # Exit
            else:
                color = "white"   # Weg

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

    root.mainloop()  # Hält das Fenster offen


if __name__ == "__main__":
    start_window()
