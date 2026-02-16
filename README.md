# 🧩 A-Maze-ing — Python Maze Generator

> A configurable and fully automated maze generator built in Python, capable of generating perfect mazes, solving them using BFS, and exporting results in hexadecimal format.

---

## 🚀 Overview

**A-Maze-ing** is a Python-based maze generation engine developed as part of the 42 curriculum.

The program:

- 🔹 Reads a configuration file  
- 🔹 Generates a random maze  
- 🔹 Embeds a visible **"42" pattern**  
- 🔹 Solves the maze using BFS  
- 🔹 Exports the maze in hexadecimal format  

This project demonstrates strong understanding of:

- Algorithms  
- Graph traversal  
- File parsing  
- Clean Python architecture  

---

## ✨ Features

- Multiple maze generation algorithms  
- Perfect maze support  
- Shortest path solver (BFS)  
- Configurable via `config.txt`  
- Hexadecimal export format  
- ASCII terminal visualization  
- Deterministic generation via seed  

---

## 🧠 Algorithms Used

### Maze Generation

- Recursive Backtracker (DFS) — default  
- Prim’s Algorithm — alternative  

### Maze Solving

- Breadth-First Search (BFS)  
  - Guarantees shortest path  
  - Efficient on grid graphs  

---

## Project Structure

```
.
├── a_maze_ing.py          # Main executable file
├── mazegen/mazegen.py     # maze generator file
├── config.txt             # Example configuration file
├── Makefile
├── README.md
├── .gitignore
├── read_config_file.py    # Reading config file
└── pyproject.toml         #Informations about the project
```

### To build the whl/tar file you can use the following command:
```
python3 -m build --no-isolation 
```

---

## Instructions

### Installation of some used packages

```bash
make install
```

---

### Run

```bash
make run
# or
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

### Lint

---

```bash
make lint
# or
make lint-strict
```

### Clean

```bash
make clean
```

---

## Configuration File

### Format

* One `KEY=VALUE` per line
* Lines starting with `#` are ignored

### Mandatory Keys Example

```
WIDTH=14
HEIGHT=14

---

ENTRY=0,0
EXIT=13,13
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Optional Key

```
SEED=42
```

A default configuration file is provided in the repository.

---

## Maze Generation Algorithm

### This project supports multiple maze generation algorithms:

1. Recursive Backtracker (DFS) (default)

2. Prim’s Algorithm (alternative)

### What Is DFS?

DFS (Depth-First Search) is a recursive backtracking algorithm that explores one path at a time, marking cells as visited and backtracking when no moves remain.

### Why DFS?

* Simple
* Easy to make **perfect** (single unique path)

For a perfect maze, DFS visits every cell once and guarantees exactly one unique path between any two cells.

### What Is Prim’s Algorithm?

Prim’s algorithm builds the maze step by step starting from one cell.
It keeps a list of nearby walls, then randomly breaks one to connect a new cell to the maze that’s already made.

### Why Prim’s?

* Makes the maze look more organic and branchy

* Has less long straight paths than DFS

* Still makes a perfect maze (only one path, no loops)

---

## Maze Solving Algorithm

### Shortest Path Solver: Breadth-First Search (BFS)

### What Is BFS?

BFS (Breadth-First Search) explores the maze cell by cell, checking all reachable cells and move on to them all until finding the exit point then give the shortest path.

### Why BFS for Solving?

* Always finds the shortest path

* Easy to reconstruct the path

* Works perfectly on grid-based mazes

---

## Output File Format

Each cell is encoded using **one hexadecimal digit**:

* `1` means wall closed
* `0` means wall open

Cells are written row by row.

After an empty line:

1. Entry coordinates
2. Exit coordinates
3. Shortest valid path using `N E S W`

---

## Visual Representation
Each cell is encoded using **one hexadecimal digit**:

* `1` means wall closed
* `0` means wall open

Cells are written row by row.

After an empty line:

1. Entry coordinates
2. Exit coordinates
3. Shortest valid path using `N E S W`

---

## Visual Representation

The maze can be displayed using:

The maze can be displayed using:

* **Terminal ASCII rendering** (default)

Features:

* regenerate maze
* show / hide shortest path
* change wall colors

---

## Resources

* https://youtu.be/sTRK9mQgYuc
* https://youtu.be/W9F8fDQj7Ok
* https://youtu.be/V1oZQm1HtVw
* https://youtu.be/sp0D2ABSaQI
* https://youtu.be/W9zSr9jnoqY
* https://youtu.be/ioUl1M77hww
* https://youtu.be/ZuHW4fS60pc
* https://youtu.be/V1oZQm1HtVw

