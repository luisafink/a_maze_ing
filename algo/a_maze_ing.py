from __future__ import annotations
import sys
from generator import MazeGenerator


def main() -> int:
    """Run the maze generator from the command line."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1

    try:
        generator = MazeGenerator.from_config_file(sys.argv[1])
        generator.generate()
        generator.write_output()

        print(generator.render_ascii(show_path=False))
        print(f"Maze written to {generator.output_file}")

    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#python3 a_maze_ing.py config.txt