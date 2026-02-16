from read_config_file import read_config
from mazegen import MazeGenerator
import random
import sys


def intro() -> None:
    print('\033c', end="")
    print("\033[35m")
    print(" █████╗       ███╗   ███╗ █████╗ ███████╗███████╗")
    print("██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝")
    print("███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗  ")
    print("██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ")
    print("██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗")
    print("╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝")
    print("\033[0m")


data = read_config()

if __name__ == "__main__":
    end = False
    Ganerate_again = 2
    retry = 0
    color = "\033[37m"
    show_path = True
    width = data["WIDTH"]
    height = data["HEIGHT"]
    entry = data["ENTRY"]
    exit_point = data["EXIT"]
    perfect = data["PERFECT"]
    seed = data["SEED"]
    anim = data["ANIMATE"]
    directions = []

    intro()
    print("Welcome to our maze Game ;)\n")
    input("\nPress ENTER to start the game...")

    while not end:
        if Ganerate_again == 2 or Ganerate_again == 3:
            if retry == 0:
                maze_seed = seed
            else:
                maze_seed = None
            maze = MazeGenerator(
                width, height, entry, exit_point, perfect, maze_seed, anim
            )
            if Ganerate_again == 2:
                maze.generate("dfs")
            elif Ganerate_again == 3:
                maze.generate("prim")
            print('\033c', end="")
            path = maze.Draw_42()
            if path is not None:
                if entry[::-1] in path or exit_point[::-1] in path:
                    print("Error: the entry or exit points is in the 42 walls")
                    sys.exit(1)
            maze.display_maze(color, None)
            path = maze.Generate_solution_bfs()
            directions = maze.Drawing_solution_path(path)
            Ganerate_again = 1
        with open(data["OUTPUT_FILE"], "w+") as output:
            for i in range(maze.height):
                for x in maze.grid[i]:
                    output.write(hex(x.walls).upper()[2:])
                output.write("\n")
            output.write("\n")
            output.write(f"{maze.entry[0]},{maze.entry[1]}\n")
            output.write(f"{maze.exit[0]},{maze.exit[1]}\n")
            output.write(''.join(directions))
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        try:
            choice = int(input("Choice? (1-4): "))
            print()
            if choice == 1:
                show_path = True
                retry += 1
                print("Avalaible algorithm's\n1- DFS")
                print("2- PRIM'S")
                choice = int(input("Chose your algorithm :) "))
                if choice == 1:
                    Ganerate_again = 2
                elif choice == 2:
                    Ganerate_again = 3
                else:
                    print("choice unavailable")
                print('\033c', end="")

            elif choice == 2:
                print('\033c', end="")
                if show_path and path is not None:
                    maze.animate_solution_path(color, path)
                    show_path = False
                else:
                    maze.display_maze(color, None)
                    show_path = True

            elif choice == 3:
                print('\033c', end="")
                A_colors = ["\033[31m", "\033[34m",
                            "\033[33m", "\033[36m", "\033[35m", "\033[37m"]
                color = random.choice(A_colors)
                if not show_path:
                    maze.display_maze(color, path)
                else:
                    maze.display_maze(color, None)
            elif choice == 4:
                end = True
            else:
                print("\n== choice unavailable :( ===\n")
        except Exception:
            print("\n==Something Wrong please try again :) ==\n")
