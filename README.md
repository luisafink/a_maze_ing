# A-Maze-ing

A maze generator written in Python. It builds a random maze from a small
config file, finds the shortest path from the entry to the exit, writes the
result to a text file, and shows it in a window where you can toggle the path,
change the wall color, or generate a new maze.

It also hides a little **"42"** drawn out of solid walls inside every maze.

---

## Requirements

- **Python 3.10+** (the code uses modern type hints)
- **Tkinter** for the window (ships with most Python installs; on some Linux
  systems install it with `sudo apt install python3-tk`)

Optional, only for the `lint` target:

```
make install
```

This installs `flake8` and `mypy`.

---

## Installation

Clone the repository:

```
git clone https://github.com/luisafink/a_maze_ing.git
cd a_maze_ing
```

There is nothing else to build — it runs straight from the source.

---

## Usage

Run it with the provided `config.txt`:

```
make run
```

or directly, without `make`:

```
python3 -m algo.a_maze_ing config.txt
```

(On Windows use `python` instead of `python3`.)

This writes the maze to the output file (`maze.txt` by default) and opens the
window.

### Window controls

| Key   | Action                              |
| ----- | ----------------------------------- |
| `p`   | Show / hide the shortest path       |
| `c`   | Cycle the wall color                |
| `r`   | Generate a new maze (next seed)     |
| `Esc` | Close the window                    |

### Make targets

| Command        | What it does                                   |
| -------------- | ---------------------------------------------- |
| `make run`     | Generate a maze and open the window            |
| `make debug`   | Run under the Python debugger (`pdb`)          |
| `make lint`    | Run `flake8` and `mypy`                        |
| `make clean`   | Remove `__pycache__` and caches                |

---

## Configuration

The maze is described by a simple `KEY=VALUE` file:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
PERFECT=True
SEED=42
OUTPUT_FILE=maze.txt
```

| Key           | Meaning                                                        |
| ------------- | ------------------------------------------------------------- |
| `WIDTH`       | Number of cells across (positive integer)                     |
| `HEIGHT`      | Number of cells down (positive integer)                       |
| `ENTRY`       | Start cell as `x,y` (0-indexed)                               |
| `EXIT`        | End cell as `x,y` (must differ from `ENTRY`)                  |
| `PERFECT`     | `True` = exactly one path between any two cells; `False` = extra openings, so the maze has loops |
| `SEED`        | Random seed for reproducible mazes (optional, default `0`)    |
| `OUTPUT_FILE` | Where to write the generated maze                             |

---

## What the code does

**`algo/`** — maze generation:

1. Reads and validates the config file.
2. Builds a grid where every cell starts fully walled in.
3. Stamps the **"42"** pattern as a block of solid cells.
4. Carves passages with a **recursive backtracker** (depth-first search).
   With `PERFECT=False` it then knocks out some extra walls to create loops,
   while making sure no fully-open 3x3 area is ever formed.
5. Runs a **breadth-first search** to find the shortest entry-to-exit path.
6. Writes the output file.

**`visual/`** — draws the maze in a Tkinter window and handles the key
controls.

### Output format

The output file looks like this:

```
<HEIGHT rows of WIDTH hex digits>   <- the maze walls
                                    <- blank line
x,y                                 <- entry
x,y                                 <- exit
NESW...                             <- shortest path as N/E/S/W moves
```

Each cell is one hex digit whose bits say which walls are present:

| Wall  | North | East | South | West |
| ----- | ----- | ---- | ----- | ---- |
| Value | 1     | 2    | 4     | 8    |

So a fully closed cell is `1+2+4+8 = 15 = F`, and a cell open to the east only
has `1+4+8 = 13 = D`.

---

## Project structure

```
a_maze_ing/
├── algo/
│   ├── a_maze_ing.py   # entry point
│   ├── generator.py    # maze generation + path finding
│   └── cell.py         # one maze cell
├── visual/
│   ├── window.py       # the Tkinter window
│   ├── render.py       # draws the whole maze
│   └── draw.py         # draws one cell
├── config.txt          # example configuration
├── maze.txt            # example output
└── Makefile
```

---

A duo project by **Luisa** and **Lejs**.
