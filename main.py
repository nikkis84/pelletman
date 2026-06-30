import pygame
from parser import load_map
from env import PelletmanEnv
from mapf_core.single_agent_planner import compute_heuristics, a_star
from ghost import move_single_ghost, move_all_ghosts
from minimax import Minimax

CELL_SIZE = 40
FPS = 5

BLACK = (20, 20, 20)
BLUE = (40, 40, 200)
WHITE = (240, 240, 240)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)
GREEN = (60, 220, 60)
GRAY = (100, 100, 100)

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


def draw_env(screen, env, font):
    rows = len(env.grid)
    cols = len(env.grid[0])

    screen.fill(BLACK)

    for r in range(rows):
        for c in range(len(env.grid[r])):
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pos = (r, c)

            if env.grid[r][c]:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

            if pos == env.goal:
                pygame.draw.rect(
                    screen,
                    GREEN,
                    (x + 8, y + 8, CELL_SIZE - 16, CELL_SIZE - 16)
                )

            if pos in env.pellets:
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    4
                )

    for ghost in env.ghosts:
        gx = ghost[1] * CELL_SIZE
        gy = ghost[0] * CELL_SIZE
        pygame.draw.circle(
            screen,
            RED,
            (gx + CELL_SIZE // 2, gy + CELL_SIZE // 2),
            CELL_SIZE // 3
        )

    px = env.pacman[1] * CELL_SIZE
    py = env.pacman[0] * CELL_SIZE
    pygame.draw.circle(
        screen,
        YELLOW,
        (px + CELL_SIZE // 2, py + CELL_SIZE // 2),
        CELL_SIZE // 3
    )

    status = f"Steps: {env.steps}   Pellets left: {len(env.pellets)}   Win: {env.win}   Done: {env.done}"
    text_surface = font.render(status, True, WHITE)
    screen.blit(text_surface, (10, rows * CELL_SIZE + 10))


def main():
    pygame.init()

    grid, pacman, ghosts, pellets, goal = load_map("maps/map4.txt")
    env = PelletmanEnv(grid, pacman, ghosts, pellets, goal)

    MAX_STEPS = 500
    pacman_minimax = Minimax(depth=3)

    rows = len(grid)
    cols = len(grid[0])

    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE + 50))
    pygame.display.set_caption("Pelletman Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    print("Initial state:")
    env.render()
    print()

    running = True
    step_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not env.done and step_count < MAX_STEPS:
            new_pacman = pacman_minimax.minimax(env)
            ghosts = move_all_ghosts(env.grid, env.ghosts, new_pacman)
            env.step(new_pacman, ghosts)

            print(f"Step {step_count + 1} | Pellets left: {len(env.pellets)}")
            env.render()
            print()

            step_count += 1

        draw_env(screen, env, font)
        pygame.display.flip()
        clock.tick(FPS)

    print("DONE:", env.done, "WIN:", env.win, "STEPS:", env.steps)
    pygame.quit()


if __name__ == "__main__":
    main()
