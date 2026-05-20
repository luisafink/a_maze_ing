PYTHON = python3
MAIN = algo/a_maze_ing.py
CONFIG = config.txt

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) -m algo.a_maze_ing $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs