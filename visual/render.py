from __future__ import annotations

import tkinter as tk

from algo.generator import MazeGenerator
from visual.draw import draw_cell, get_cell_color


def render_maze(
    canvas: tk.Canvas,
    generator: MazeGenerator,
    tile_size: int,
    wall_color: str,
    show_path: bool,
) -> None:
    """Render the full maze."""
    canvas.delete("all")

    path_cells = (
        generator._path_cells()
        if show_path
        else set()
    )

    for y in range(generator.height):
        for x in range(generator.width):
            cell = generator.maze[x][y]

            color = get_cell_color(
                (x, y),
                generator.entry,
                generator.exit_cell,
                generator.pattern_cells,
                path_cells,
                show_path,
            )

            draw_cell(
                canvas,
                cell,
                x,
                y,
                tile_size,
                wall_color,
                color,
            )
