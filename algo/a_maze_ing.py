from __future__ import annotations
import sys
from algo.generator import MazeGenerator
from visual.window import start_window


def main() -> int:
    """Run the maze generator from the command line."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1

    try:
        generator = MazeGenerator.from_config_file(sys.argv[1])
        generator.generate()
        generator.write_output()

        print(f"Maze written to {generator.output_file}")

        start_window(generator)

    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
