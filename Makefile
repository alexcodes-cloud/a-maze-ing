PIP = pip3
PYT = python3
FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
SRC = a_maze_ing.py config.txt
RM = rm -rf
CACHE = __pycache__ .mypy_cache

run:
	$(PYT) $(SRC)

install:
	$(PIP) install flake8
	$(PIP) install mypy
	$(PIP) install typing

debug:
	$(PYT) -m pdb $(SRC)

clean:
	$(RM) $(CACHE)
	$(RM) mazegen/__pycache__ mazegen/.mypy_cache

lint:
	flake8 .
	mypy . $(FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict