from __future__ import annotations

import tkinter as tk

from algo.generator import MazeGenerator
from visual.render import render_maze


class MazeWindow:
    """Tkinter window for maze visualization."""

    def __init__(self, generator: MazeGenerator) -> None:
        self.generator = generator
        self.show_path = True
        self.wall_colors = ["black", "blue", "red", "purple"]
        self.wall_color_index = 0

        self.root = tk.Tk()
        self.root.title("A-Maze-ing")
        self.root.configure(background="white")

        self.tile_size = self._get_tile_size()
        self.width_px = self.generator.width * self.tile_size
        self.height_px = self.generator.height * self.tile_size

        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=self.width_px,
            height=self.height_px,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.label = tk.Label(
            self.root,
            text="p = path | c = color | r = regenerate | esc = quit",
            background="white",
        )
        self.label.grid(row=1, column=0, sticky="ew")

        self.root.bind("p", self.toggle_path)
        self.root.bind("c", self.change_wall_color)
        self.root.bind("r", self.regenerate_maze)
        self.root.bind("<Escape>", self.quit)

        self.root.update_idletasks()
        label_height = self.label.winfo_reqheight()
        self.root.geometry(f"{self.width_px}x{self.height_px + label_height}")
        self.draw()
        self.root.after_idle(self.draw)

    def _get_tile_size(self) -> int:
        """Return fitting tile size."""
        return max(
            15,
            min(
                700 // self.generator.width,
                700 // self.generator.height,
            ),
        )

    def draw(self) -> None:
        """Draw the maze."""
        render_maze(
            self.canvas,
            self.generator,
            self.tile_size,
            self.wall_colors[self.wall_color_index],
            self.show_path,
        )
        self.canvas.update_idletasks()

    def toggle_path(self, event: tk.Event) -> None:
        """Show or hide shortest path."""
        self.show_path = not self.show_path
        self.draw()

    def change_wall_color(self, event: tk.Event) -> None:
        """Change wall color."""
        self.wall_color_index += 1
        self.wall_color_index %= len(self.wall_colors)
        self.draw()

    def regenerate_maze(self, event: tk.Event) -> None:
        """Generate a new maze."""
        self.generator.seed += 1
        self.generator.generate()
        self.generator.write_output()
        self.draw()

    def quit(self, event: tk.Event) -> None:
        """Close the window."""
        self.root.destroy()

    def run(self) -> None:
        """Start tkinter loop."""
        self.root.mainloop()


def start_window(generator: MazeGenerator) -> None:
    """Start maze window."""
    window = MazeWindow(generator)
    window.run()
