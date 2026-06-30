from enum import Enum
import copy
class PelletmanEnv:
    def __init__(self, grid, pacman, ghosts, pellets, goal,steps=0):
        self.grid = grid
        self.pacman = pacman
        self.ghosts = ghosts
        self.pellets = set(pellets)
        self.goal = goal
        self.steps = steps
        self.done = False
        self.win = False


    def is_wall(self, pos):
        r, c = pos
        return self.grid[r][c]

    def step(self, new_pacman, new_ghosts):
        if self.done:
            return

        self.steps += 1

        self.pacman = new_pacman
        self.ghosts = new_ghosts

        if self.pacman in self.ghosts:
            self.done = True
            self.win = False
            # print("Pacman caught by ghost!")
            return

        if self.pacman in self.pellets:
            self.pellets.remove(self.pacman)

        if not self.pellets and self.pacman == self.goal:
            self.done = True
            self.win = True
            # print("All pellets eaten and goal reached!")

    def render(self):
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows else 0
        ghost_set = set(self.ghosts)

        for r in range(rows):
            line = ""
            for c in range(len(self.grid[r])):
                pos = (r, c)
                if self.grid[r][c]:
                    line += "#"
                elif pos == self.pacman:
                    line += "P"
                elif pos in ghost_set:
                    line += "X"
                elif pos in self.pellets:
                    line += "."
                elif pos == self.goal:
                    line += "G"
                else:
                    line += " "
            print(line)

    class Directions(Enum):
        UP = (-1, 0)
        DOWN = (1, 0)
        LEFT = (0, -1)
        RIGHT = (0, 1)
        # STAY = (0,0)

    def successors(self, agent_idx):
        successors = []
        if(agent_idx==0):
            pos = self.pacman
        else:
            pos = self.ghosts[agent_idx-1]

        for direction in self.Directions:
            dir_r, dir_c = direction.value
            update_r = pos[0]+dir_r
            update_c = pos[1]+dir_c
            updated_pos = (update_r, update_c)


            if 0 <= update_r < len(self.grid) and 0 <=update_c < len(self.grid[0]):
                if not self.is_wall(updated_pos):
                    future_pacman = self.pacman
                    future_ghosts = list(self.ghosts)
                    if agent_idx == 0:
                        future_pacman = updated_pos
                    else:
                        future_ghosts[agent_idx-1] = updated_pos
                    
                    future_state = PelletmanEnv(
                        self.grid, 
                        future_pacman, 
                        tuple(future_ghosts), 
                        self.pellets.copy(), 
                        self.goal,
                        self.steps)
                    future_state.step(future_state.pacman, tuple(future_ghosts))
            
                    successors.append((direction,future_state))

        return successors


def manhattan_distance(coord1, coord2):
    return abs(coord1[0]-coord2[0]) + abs(coord1[1]-coord2[1])


def eval_func(state):
    # Give high val for maximizer, and low val if minimizer
    if state.win:
        # return float('inf')
        return 50000
    if state.done:
        # return -float('inf')
        return -50000 
    
    # if state.pacman in state.pellets:
    #     return 100

    f1 =0
    f2 =0
    f3 =0
    f4=0
    #f1 pellets_dist
    if state.pellets:
        pellet_distances = []
        for pellet_loc in state.pellets:
            pellet_distances.append(manhattan_distance(state.pacman, pellet_loc))
        f1= min(pellet_distances)
 
    #f2 goal
    if not state.pellets: # no more pellets go to goal
        f2= manhattan_distance(state.pacman, state.goal)

    #f3 ghosts
    ghost_distances = []
    for ghost_loc in state.ghosts:
        ghost_distances.append(manhattan_distance(state.pacman, ghost_loc))
    f3= min(ghost_distances)

    #f3 pellets
    # if len(state.pellets) >0:
    f4= len(state.pellets)
    
    # if a ghost is too close, gets rid of it oscillating when ghost is far
    if f3 < 2:
        return -50000 +  (state.steps * 10)
     
  

    w1 = -12
    w2 = -15
    w3 = 400
    w4 = -200

      #if ghost is far
    if f3 > 5:
        w3 = 20

    #still pellets ignore goal
    if state.pellets:
        f2 = 0 
    
    eval = w1*f1 + w2*f2 + w3*f3+ w4*f4 
    if state.pellets:
        eval -= 2 * f1

    if f3 < 2:
        eval -=500
    eval -= 5
    return eval

