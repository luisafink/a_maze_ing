from __future__ import annotations

import tkinter as tk

from algo.generator import EAST, SOUTH

Coord = tuple[int, int]


def get_cell_color(
    coord: Coord,
    entry: Coord,
    exit_cell: Coord,
    pattern_cells: set[Coord],
    path_cells: set[Coord],
    show_path: bool,
) -> str:
    """Return the fill color for one cell."""
    if coord == entry:
        return "green"

    if coord == exit_cell:
        return "red"

    if coord in pattern_cells:
        return "gray"

    if show_path and coord in path_cells:
        return "lightblue"

    return "white"


def draw_cell(
    canvas: tk.Canvas,
    cell,
    x: int,
    y: int,
    tile_size: int,
    wall_color: str,
    color: str,
) -> None:
    """Draw one maze cell."""
    x1 = x * tile_size
    y1 = y * tile_size
    x2 = x1 + tile_size
    y2 = y1 + tile_size

    canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill=color,
        outline="",
    )

    if cell.wall & EAST:
        canvas.create_line(
            x2,
            y1,
            x2,
            y2,
            width=3,
            fill=wall_color,
        )

    if cell.wall & SOUTH:
        canvas.create_line(
            x1,
            y2,
            x2,
            y2,
            width=3,
            fill=wall_color,
        )

    if x == 0:
        canvas.create_line(
            x1,
            y1,
            x1,
            y2,
            width=3,
            fill=wall_color,
        )

    if y == 0:
        canvas.create_line(
            x1,
            y1,
            x2,
            y1,
            width=3,
            fill=wall_color,
        )
