import sys
from typing import Any


def error(msg: str) -> None:
    """ Display an error message and terminate the program."""
    print(f"Error: {msg}")
    sys.exit(1)


def read_config() -> dict[str, Any]:
    if len(sys.argv) != 2:
        """ Read and validate the maze configuration file."""
        error("Usage: python3 a_maze_ing.py config.txt")

    filename = sys.argv[1]

    try:
        file = open(filename, "r")
    except (FileNotFoundError, PermissionError):
        error(f"Cannot open config file: {filename}")

    config: dict[str, Any] = {}

    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            error(f"Invalid config line: {line}")
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()
    file.close()
    required = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    for key in required:
        if key not in config:
            error(f"Missing required key: {key}")
    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])
    except ValueError:
        error("WIDTH and HEIGHT must be integers value ;)")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        error("WIDTH and HEIGHT must be > 0")
    if config["WIDTH"] < 10 or config["HEIGHT"] < 10:
        error("Sorry the maze too small to display " +
              "the entire 42 pattern :(")
    try:
        ex, ey = config["ENTRY"].split(",")
        config["ENTRY"] = (int(ex), int(ey))

        xi, yi = config["EXIT"].split(",")
        config["EXIT"] = (int(xi), int(yi))
        if (
            int(ex) < 0
            or int(ex) >= config["WIDTH"]
            or int(ey) < 0
            or int(ey) >= config["HEIGHT"]
        ):
            error("the entry points are out of range")
        if (
            int(xi) < 0
            or int(xi) >= config["WIDTH"]
            or int(yi) < 0
            or int(yi) >= config["HEIGHT"]
        ):
            error("the exit points are out of range")

    except ValueError:
        error("ENTRY and EXIT must be in format x,y")

    if config["ENTRY"] == config["EXIT"]:
        error("The entry point and exit cannot be at the same place")
    if config["PERFECT"].lower() == "true":
        config["PERFECT"] = True
    elif config["PERFECT"].lower() == "false":
        config["PERFECT"] = False
    else:
        error("PERFECT must be True or False Only ;)")

    if not config["OUTPUT_FILE"]:
        error("no output file has been added ;)")
    if not config["OUTPUT_FILE"][0].isalpha():
        error("Wrong file name ! (ex: maze.txt)")

    if "SEED" in config:
        try:
            config["SEED"] = int(config["SEED"])
        except ValueError:
            error("SEED must be an integer")
    else:
        config["SEED"] = None

    if "ANIMATE" in config:
        if config["ANIMATE"].lower() == "true":
            config["ANIMATE"] = True
        elif config["ANIMATE"].lower() == "false":
            config["ANIMATE"] = False
        else:
            error("The ANIMATE value must be true or false :(")
    else:
        config["ANIMATE"] = True

    return config
