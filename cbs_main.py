from parser import load_map
from env import PelletmanEnv
from mapf_core.cbs import CBSSolver
from mapf_core.single_agent_planner import compute_heuristics


def nearest_pellet(pacman, pellets, grid):
    reachable = []

    for pellet in pellets:
        h = compute_heuristics(grid, pellet)
        if pacman in h:
            reachable.append((h[pacman], pellet))

    if not reachable:
        return None

    reachable.sort()
    return reachable[0][1]


def next_pos(path):
    return path[1] if len(path) > 1 else path[0]


def main():
    grid, pacman, ghosts, pellets, goal = load_map("maps/map1.txt")
    env = PelletmanEnv(grid, pacman, ghosts, pellets, goal)

    MAX_STEPS = 500

    for t in range(MAX_STEPS):
        if env.done:
            break

        if env.pellets:
            pac_goal = nearest_pellet(env.pacman, env.pellets, env.grid)
            if pac_goal is None:
                print("No reachable pellets left.")
                break
        else:
            if env.goal is None:
                print("Error: no G tile found in map.")
                break
            pac_goal = env.goal

        ghost_goals = [env.pacman for _ in env.ghosts]

        starts = [env.pacman] + env.ghosts
        goals = [pac_goal] + ghost_goals

        solver = CBSSolver(env.grid, starts, goals)
        paths = solver.find_solution(disjoint=False)

        if paths is None:
            print("CBS returned None (time limit hit / no solution).")
            break

        new_positions = [next_pos(p) for p in paths]
        new_pacman = new_positions[0]
        new_ghosts = new_positions[1:]

        env.step(new_pacman, new_ghosts)

        print(f"\nStep {t + 1} | Pac goal: {pac_goal} | Pellets left: {len(env.pellets)}")
        print("Pacman:", env.pacman, "Ghosts:", env.ghosts)
        env.render()

    print("\nDONE:", env.done, "WIN:", env.win, "STEPS:", env.steps)


if __name__ == "__main__":
    main()