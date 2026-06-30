from env import eval_func
from ghost import move_single_ghost, move_all_ghosts
from env import PelletmanEnv
import random
class Minimax:
    def __init__(self, depth=3):
        self.depth = depth

    def value(self, state, depth, agent_idx, alpha, beta):
        #if the state is a terminal state: return the state's utility
        #if the next agent is MAX: return max-value(state)
        #if the next agent is MIN: return min-value(state)
        if state.done or depth == 0:
            return eval_func(state)
        if agent_idx == 0: #maximizing agent
            return self.max_value(state, depth, alpha, beta)
        else:
            return self.min_value(state, depth, agent_idx, alpha, beta)

    def max_value(self, state, depth, alpha, beta):
        v = -float('inf')
        for action, successor in state.successors(0):
            v = max(v, self.value(successor, depth, 1, alpha, beta))
            if v>= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, depth, agent_idx, alpha, beta):
        v = float('inf')
        num_agents = 1 + len(state.ghosts)

        # (Action i.e. UP, DOWN, LEFT, RIGHT, state)- could remove action here?
        for action, successor in state.successors(agent_idx):
            if agent_idx == num_agents - 1:
                score = min(v, self.value(successor, depth - 1, 0, alpha, beta))
            else:
                score = min(v, self.value(successor, depth, agent_idx + 1, alpha, beta))
            v = min(v, score)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
        
    
    def minimax(self, env):
        successors = env.successors(0)
        minimax_score = -float('inf')
        minimax_successor = None
        best_moves=[]
        alpha = -float('inf')
        beta = float('inf')
        for action, successor in successors:
            curr_score = self.value(successor, self.depth-1, 1, alpha, beta)
            if curr_score > minimax_score:
                minimax_score = curr_score
                minimax_successor = successor
            # elif curr_score == minimax_score:
            #     if random.random() < 0.5:
            #         minimax_successor=successor
        
            alpha = max(alpha, minimax_score)
        if minimax_successor:
            return minimax_successor.pacman
        else:
            return env.pacman
        

