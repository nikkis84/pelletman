from mapf_core.single_agent_planner import compute_heuristics, a_star

def next_pos(path):
    return path[1] if path is not None and len(path) > 1 else path[0] if path else None

def move_single_ghost(grid, ghost_pos, pacman_pos):
    h_values = compute_heuristics(grid, pacman_pos)

    path = a_star(
        grid,
        ghost_pos,
        pacman_pos,
        h_values,
        0,
        []
    )

    if path is None:
        return ghost_pos

    nxt = next_pos(path)
    return nxt if nxt is not None else ghost_pos


def move_all_ghosts(grid, ghosts, pacman_pos):
    new_ghosts = []

    for ghost in ghosts:
        new_ghost = move_single_ghost(grid, ghost, pacman_pos)
        new_ghosts.append(new_ghost)

    return new_ghosts