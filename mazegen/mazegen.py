import random
from collections import deque
import time


class MazeGenerator:
    """MazeGenerator is responsible for creating, generating, displaying,
       and solving mazes."""
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
        anim: bool = False
    ) -> None:
        """Initialize a MazeGenerator instance."""

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.anim = anim
        self.generation_steps: list[tuple[int, int, str]] = []

        self.rng = random.Random(seed)

        self.grid = []
        for _ in range(height):
            rows = []
            for _ in range(width):
                rows.append(Cell())
            self.grid.append(rows)

    def Draw_42(self) -> list[tuple[int, int]] | None:
        """Draws the '42' wall pattern inside the maze."""
        if self.height >= 10 and self.width >= 10:
            width = int((self.width - 7) / 2)
            height = int((self.height - 5) / 2)
            walls_42 = [(height, width), (height+1, width),
                        (height+2, width), (height+2, width+1),
                        (height+2, width+2), (height+1, width+2),
                        (height, width+2), (height+3, width+2),
                        (height+4, width+2), (height+4, width+4),
                        (height+4, width+5), (height+4, width+6),
                        (height+3, width+4), (height+2, width+4),
                        (height+2, width+5), (height+2, width+6),
                        (height+1, width+6), (height, width+6),
                        (height, width+5), (height, width+4),]
            return walls_42
        return None

    def check_available_wall(self, x: int, y: int) -> bool:
        """Check whether a cell coordinate is inside the maze boundaries."""
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        return False

    def remove_wall(self, x: int, y: int, direction: str) -> None:
        """Remove a wall from a cell in a given direction."""
        cell = self.grid[y][x]

        if direction == "N":
            cell.walls &= 0b1110
        elif direction == "E":
            cell.walls &= 0b1101
        elif direction == "S":
            cell.walls &= 0b1011
        elif direction == "W":
            cell.walls &= 0b0111

    def remove_opposite_wall(self, x: int, y: int, direction: str) -> None:
        """Remove the wall between a cell and its neighboring cell
        in the given direction."""
        if direction == "N" and self.check_available_wall(x, y-1):
            self.remove_wall(x, y, "N")
            self.remove_wall(x, y-1, "S")
        elif direction == "E" and self.check_available_wall(x+1, y):
            self.remove_wall(x, y, "E")
            self.remove_wall(x+1, y, "W")
        elif direction == "S" and self.check_available_wall(x, y+1):
            self.remove_wall(x, y, "S")
            self.remove_wall(x, y+1, "N")
        elif direction == "W" and self.check_available_wall(x-1, y):
            self.remove_wall(x, y, "W")
            self.remove_wall(x-1, y, "E")

    def get_available_unvisited_walls(self, x: int, y: int) \
            -> list[tuple[int, int, str]]:
        """Get all unvisited neighboring cells reachable from the
        current cell."""
        directions = ["N", "E", "S", "W"]
        unvisited_walls = []
        for dir in directions:
            if dir == "N" and self.check_available_wall(x, y-1) \
                    and not self.grid[y-1][x].is_visited:
                unvisited_walls.append((x, y-1, "N"))
            elif dir == "E" and self.check_available_wall(x+1, y) \
                    and not self.grid[y][x+1].is_visited:
                unvisited_walls.append((x+1, y, "E"))
            elif dir == "S" and self.check_available_wall(x, y+1) \
                    and not self.grid[y+1][x].is_visited:
                unvisited_walls.append((x, y+1, "S"))
            elif dir == "W" and self.check_available_wall(x-1, y) \
                    and not self.grid[y][x-1].is_visited:
                unvisited_walls.append((x-1, y, "W"))
        return unvisited_walls

    def remove_visited_walls(self) -> None:
        """ Reset the visited state of all cells in the maze."""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].is_visited = False

    def generate(self, algo: str = 'dfs') -> None:
        """Generate the maze using the specified algorithm."""
        walls = self.Draw_42()

        if walls is not None:
            for y, x in walls:
                self.grid[y][x].is_visited = True
        if algo == "dfs":
            self.grid[0][0].is_visited = True
            self.dfs(0, 0, self.anim)
        elif algo == "prim":
            self.grid[0][0].is_visited = True
            self.prim(0, 0, self.anim)
        if not self.perfect and walls is not None:
            self.remove_visited_walls()
            for y, x in walls:
                self.grid[y][x].is_visited = True
            if algo == "dfs":
                self.dfs(0, 0, self.anim)
            elif algo == "prim":
                self.prim(0, 0, self.anim)

    def dfs(
            self,
            x: int,
            y: int,
            animate: bool = True
            ) -> None:
        """Generate the maze using the Depth-First Search (DFS) algorithm."""

        while True:
            available_walls = self.get_available_unvisited_walls(x, y)
            if not available_walls:
                return
            choice = self.rng.choice(available_walls)
            nx, ny, direction = choice

            self.grid[ny][nx].is_visited = True
            self.remove_opposite_wall(x, y, direction)

            if animate:
                self.generation_steps.append((x, y, direction))

            self.dfs(nx, ny, animate)

    def prim(
            self,
            s_x: int,
            s_y: int,
            animate: bool = True,
            ) -> None:
        """Generate the maze using Prim's algorithm."""

        walls = []

        self.grid[s_y][s_x].is_visited = True

        walls.extend(self.get_available_unvisited_walls(s_x, s_y))

        while walls:
            nx, ny, direction = random.choice(walls)
            walls.remove((nx, ny, direction))

            if self.grid[ny][nx].is_visited:
                continue

            if direction == "N":
                self.remove_opposite_wall(nx, ny, "S")
                if animate:
                    self.generation_steps.append((nx, ny, "S"))
            elif direction == "E":
                self.remove_opposite_wall(nx, ny, "W")
                if animate:
                    self.generation_steps.append((nx, ny, "W"))
            elif direction == "S":
                self.remove_opposite_wall(nx, ny, "N")
                if animate:
                    self.generation_steps.append((nx, ny, "N"))
            elif direction == "W":
                self.remove_opposite_wall(nx, ny, "E")
                if animate:
                    self.generation_steps.append((nx, ny, "E"))

            self.grid[ny][nx].is_visited = True

            walls.extend(self.get_available_unvisited_walls(nx, ny))

    def Generate_solution_bfs(self) -> list[tuple[int, int]]:
        """Generate a solution path from entry to exit using
        the Breadth-First Search (BFS) algorithm."""
        start = self.entry
        end = self.exit

        queue = deque([start])
        visited = set([start])
        parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                break

            cell = self.grid[y][x]

            # NORTH
            if cell.walls & 0b0001 == 0 and y > 0:
                nx, ny = x, y - 1
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # EAST
            if cell.walls & 0b0010 == 0 and x < self.width - 1:
                nx, ny = x + 1, y
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # SOUTH
            if cell.walls & 0b0100 == 0 and y < self.height - 1:
                nx, ny = x, y + 1
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # WEST
            if cell.walls & 0b1000 == 0 and x > 0:
                nx, ny = x - 1, y
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        path = []
        current: tuple[int, int] | None = end
        while current is not None:
            path.append(current)
            current = parent[current]

        path.reverse()
        return path

    def Drawing_solution_path(
            self,
            path: list[tuple[int, int]] | None
            ) -> list[str]:
        """Convert a solution path into a list of movement directions."""

        directins = []
        if path is not None:
            index = 0
            for x, y in path:
                index += 1
                if index >= len(path):
                    break
                nx, ny = path[index]
                if nx == x + 1:
                    directins.append("E")
                elif nx == x - 1:
                    directins.append("W")
                if ny == y + 1:
                    directins.append("S")
                elif ny == y - 1:
                    directins.append("N")
        return directins

    def animate_solution_path(
        self,
        color: str,
        path: list[tuple[int, int]],
        delay: float = 0.08
    ) -> None:
        """Animate the solution path from entry to exit."""
        animated: list[tuple[int, int]] = []

        for step in path:
            animated.append(step)
            print("\033[H\033[J", end="")
            self.draw_maze(color, animated)
            time.sleep(delay)

    def reset_grid_walls(self) -> None:
        """Reset all cells to initial wall state"""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                cell.walls = 0b1111
                cell.is_visited = False

    def display_maze(
            self,
            color: str = "\033[37m",
            path: list[tuple[int, int]] | None = None,
            delay: float = 0.01) -> None:
        """control the display if with animation or not ."""
        if self.anim and self.generation_steps:
            self.reset_grid_walls()
            for x, y, direction in self.generation_steps:
                self.remove_opposite_wall(x, y, direction)
                print("\033[H\033[J", end="")
                self.draw_maze(color, None)
                time.sleep(delay)
            print('\033c', end="")
            self.draw_maze(color, path)

            self.generation_steps.clear()
            return
        self.draw_maze(color, None)

    def draw_maze(self, color: str,
                  path: list[tuple[int, int]] | None = None) -> None:
        """Display the maze in the terminal."""

        wall_42 = self.Draw_42()
        RESET = "\033[0m"
        print(color + "█" + "████" * self.width + RESET)
        wall_42_is_excite = True
        if self.height < 10 or self.width < 10:
            wall_42_is_excite = False
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if (x, y) == self.entry:
                    if cell.walls & 0b1000:
                        print(color + "█🟢 " + RESET, end="")
                    else:
                        print(" 🟢 ", end="")

                elif (wall_42_is_excite and wall_42 is not None
                      and (y, x) in wall_42):

                    print(color + "█" + RESET, end="")
                    print("\033[90m" "███" + RESET, end="")
                elif (x, y) == self.exit:
                    if cell.walls & 0b1000:
                        print(color + "█🔴 " + RESET, end="")
                    else:
                        print("🔴  ", end="")
                elif cell.walls & 0b1000:
                    if path is not None and (x, y) in path:
                        print(color + "█" + RESET, end="")
                        print("\033[32m" "███" + RESET, end="")
                    else:
                        print(color + "█" + RESET, end="")
                        print("   ", end="")
                elif cell.walls & 0b1000 == 0:
                    if path is not None and (x, y) in path:
                        if (x - 1, y) not in path:
                            print("\033[32m" " ███" + RESET, end="")
                        else:
                            print("\033[32m" "████" + RESET, end="")
                    else:
                        print(" ", end="")
                        print("   ", end="")

            print(color + "█" + RESET)
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.walls & 0b0100:
                    print(color + "████" + RESET, end="")
                else:
                    if path is not None and (x, y) in path:
                        if (x, y + 1) not in path:
                            print(color + "█" + "\033[32m" + "   " + RESET,
                                  end="")
                        else:
                            print(color + "█" + "\033[32m" + "███" + RESET,
                                  end="")
                    else:
                        print(color + "█   " + RESET, end="")
            print(color + "█" + RESET)


class Cell:
    """Represent a single cell in the maze grid."""
    def __init__(self) -> None:
        """Initialize a maze cell."""
        self.walls = 0b1111
        self.is_visited = False
