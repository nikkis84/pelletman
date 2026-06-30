def load_map(filename="maps/map1.txt"):
    grid = []
    pacman = None
    ghosts = []
    pellets = set()
    goal = None

    with open(filename, "r") as f:
        lines = [line.rstrip("\n") for line in f]

    for r, line in enumerate(lines):
        row = []
        for c, ch in enumerate(line):
            if ch == "#":
                row.append(True)
            else:
                row.append(False)

                if ch == "P":
                    pacman = (r, c)
                elif ch in ["1", "2", "3"]:
                    ghosts.append((r, c))
                elif ch == ".":
                    pellets.add((r, c))
                elif ch == "G":
                    goal = (r, c)

        grid.append(row)

    return grid, pacman, ghosts, pellets, goal