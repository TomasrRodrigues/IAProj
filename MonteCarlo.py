import math
import random
from GameState import GameState

class MonteCarloNode:
    def __init__(self, state, parent=None, move=None, last_play=None, simulation_depth=20):
        self.state = state.copy_state()
        self.parent = parent
        self.move = move
        self.last_play = last_play
        self.children = []
        self.untried_moves = None
        self.visits = 0
        self.total_reward = 0.0
        self.simulation_depth = simulation_depth  # Depth parameter

    def is_fully_expanded(self):
        if self.untried_moves is None:
            self.untried_moves = self.state.get_valid_plays()
        return len(self.untried_moves) == 0

    def select_child(self, exploration_param=1.4):
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            if child.visits == 0:
                score = float('inf')
            else:
                exploitation = child.total_reward / child.visits
                exploration = exploration_param * math.sqrt(math.log(self.visits) / child.visits)
                score = exploitation + exploration
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self):
        if self.untried_moves is None:
            self.untried_moves = self.state.get_valid_plays()
        if not self.untried_moves:
            return None
        move = self.untried_moves.pop()
        new_state, last_play = self.apply_move(move)
        child = MonteCarloNode(
            new_state,
            parent=self,
            move=move,
            last_play=move,
            simulation_depth=self.simulation_depth  # Inherit depth
        )
        self.children.append(child)
        return child

    def apply_move(self, move):
        new_state = self.state.copy_state()
        if move[0] == 'move':
            new_state = new_state.make_move(move)
        elif move[0] == 'place':
            new_state = new_state.place_piece(move[1], new_state.current_player)
        new_state.current_player = "white" if new_state.current_player == "black" else "black"
        return new_state, move

    def is_terminal(self):
        return self.state.is_game_over(self.last_play)

    def simulate(self, ai_color):
        current_state = self.state.copy_state()
        last_play = self.last_play
        steps = 0
        while steps < self.simulation_depth:  # Use parameterized depth
            if current_state.is_game_over(last_play):
                break
            valid_moves = current_state.get_valid_plays()
            if not valid_moves:
                break
            move = self.choose_heuristic_move(current_state, valid_moves, ai_color)
            if move[0] == 'move':
                new_state = current_state.make_move(move)
            elif move[0] == 'place':
                new_state = current_state.place_piece(move[1], current_state.current_player)
            new_state.current_player = "white" if new_state.current_player == "black" else "black"
            last_play = move
            current_state = new_state
            steps += 1

        if current_state.is_game_over(last_play):
            losing_color = current_state.check_lose()
            if losing_color is not None:
                winner = 'white' if losing_color == 'black' else 'black'
            else:
                winner = current_state.check_win(last_play) if last_play and last_play[0] == 'move' else None
            reward = 1.0 if winner == ai_color else -1.0 if winner else 0.0
        else:
            last_was_move = last_play[0] == 'move' if last_play else False
            reward = current_state.evaluate_board(last_was_move, ai_color) / 1000
        return reward

    def choose_heuristic_move(self, state, valid_moves, ai_color):
        opponent = "white" if ai_color == "black" else "black"
        for move in valid_moves:
            if move[0] == 'move':
                dest = move[2]
                if self.is_blocking_opponent_win(state, dest, opponent):
                    return move
            elif move[0] == 'place':
                if self.is_central_placement(move[1]):
                    return move
        return random.choice(valid_moves)

    def is_blocking_opponent_win(self, state, dest, opponent):
        temp_state = state.copy_state()
        temp_state.pieces.append((dest, opponent))
        return temp_state.check_lose() == opponent

    def is_central_placement(self, tile):
        return (2 <= tile[0] <= 4) and (2 <= tile[1] <= 4)

def montecarlo(state, simulations, ai_color, simulation_depth=20):
    root = MonteCarloNode(
        state.copy_state(),
        simulation_depth=simulation_depth
    )

    for _ in range(simulations):
        node = root
        while True:
            if node.is_terminal():
                break
            if not node.is_fully_expanded():
                child = node.expand()
                if child:
                    node = child
                break
            else:
                node = node.select_child()

        reward = node.simulate(ai_color)

        current_node = node
        while current_node is not None:
            current_node.visits += 1
            current_node.total_reward += reward
            current_node = current_node.parent
            reward *= 0.95  # Reward discounting

    if not root.children:
        return None

    best_move = max(root.children, key=lambda c: c.visits + (c.total_reward/c.visits if c.visits >0 else 0))
    return best_move.move