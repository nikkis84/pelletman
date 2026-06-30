
# 1. `minimax.py` Documentation

## Objective
Minimax is used to decide the **best move for Pacman** by simulating future moves.

## Idea
- Pacman = MAX player** (tries to maximize score)
- Ghosts = **MIN player / environment** (tries to reduce score)

##Class: `Minimax`

## How it works

1. Pacman considers all possible moves
2. For each move:
   - Simulate ghost movement
   - Recursively evaluate future states
3. Choose the move with the **highest score**

---

## Key Functions

### `value(state, depth, agent_idx)`
- Controls recursion
- Stops when:
  - Game ends (`state.done`)
  - Depth limit reached
        -Use evaluation function
- #if the state is a terminal state: return the state's utility
- #if the next agent is MAX: return max-value(state)
- #if the next agent is MIN: return min-value(state)

---

### `max_value(state, depth)`
- Pacman’s turn
- Chooses the **maximum value** among successors

    -Pseudocode from slides
    ```python 
        def max-value(state):
        initialize v = -∞
        for each successor of state:
        v = max(v, min-value(successor))
        return v
    ```




### `min_value(state, depth)`
-Ghosts move 
- Chooses the **minimum value** among successors

    -Pseudocode from slides
    ```python 
        def min-value(state):
        initialize v = +∞
        for each successor of state:
        v = min(v, max-value(successor))
        return v
    ```
    
### `minimax(self, env):`
-After going through all successors (possible moves) Chooses the next best move, picks the action that produced the highest score. That will
be the position pacman takes




# 2. `env.py - successor(self, agent_idx) & eval_func(state)` Documentation

# Successor Function

## Purpose
The successor function generates all possible **next states** from the current state.

It is used by Minimax to explore different future possibilities.

---

## Directions 
-(Possible directions that Pacman can take)

```python
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
```
---

## How it works:
1. Identify Current agent with agent_idx (0 for Pacman, >0 for Ghosts)
2. Try all directions
    -`for direction in self.Directions:` `update_r = pos[0] + dir_r`, `update_c = pos[1] + dir_c`
3. Check valid moves (if inside grid and not a wall)
4. Create a future state (copy current state, update the positions of Pacman or ghosts)
    -`future_state = PelletmanEnv(...)`
5. Simulate the move
    -`future_state.step(...)`
6. Store the successor





# Evaluation Function

## Purpose
The evaluation function assigns a **score to a state**.

It is used when:
- The search reaches maximum depth
- The game ends
---
## Function from slides
Eval(s) = w1f1(s) + w2f2(s) +...+ wnfn(s)
    E.g. From chess f1(s) = (num white queen - num black queen) 
---

## Terminal States

```python
if state.win:
    return 1000000

if state.done:
    return -1000000
```
## Features Used
-f1: distance to pellets
-f2: distance to goal
-f3: distance to ghosts
-f4: remaining pellets

-w1: weight for distance to pellets
-w2: weight for distance to goal
-w3: weight for distance to ghosts
-w4: weight for remaining pellets

` eval = w1*f1 + w2*f2 + w3*f3+ w4*f4 `