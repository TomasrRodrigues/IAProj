# montecarlo.py
import math
import random
import copy

UCT_CONSTANT = 1.414
EPSILON = 0.2  # probability of choosing the best heuristic move in rollout

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.untried_moves = state.get_valid_plays()
        self.visits = 0
        self.total_reward = 0

    def uct_select_child(self):
        return max(self.children, key=lambda child: child.total_reward / child.visits +
                   UCT_CONSTANT * math.sqrt(math.log(self.visits) / child.visits))

    def expand(self):
        move = self.untried_moves.pop()
        if move[0] == "move":
            new_state = self.state.make_move(move)
            last_move = True
        elif move[0] == "place":
            new_state = self.state.place_piece(move[1], self.state.current_player)
            last_move = False
        else:
            new_state = copy.deepcopy(self.state)
            last_move = False
        child_node = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node, last_move

    def update(self, reward):
        self.visits += 1
        self.total_reward += reward
        if self.parent is not None:
            self.parent.update(reward)

def rollout_policy(state):
    valid_moves = state.get_valid_plays()
    if not valid_moves:
        return None
    if random.random() < EPSILON:
        # Heuristic: For example, choose the move that minimizes the opponent's win chance.
        # Here we simply evaluate each move using the state's evaluate_board.
        best_move = None
        best_score = -math.inf if state.current_player == "white" else math.inf
        for move in valid_moves:
            if move[0] == "move":
                new_state = state.make_move(move)
                last = True
            elif move[0] == "place":
                new_state = state.place_piece(move[1], state.current_player)
                last = False
            score = new_state.evaluate_board(last)
            if state.current_player == "white":
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move
    else:
        return random.choice(valid_moves)

def safe_rollout_policy(state):

    valid_moves = state.get_valid_plays()
    if not valid_moves:
        return None

    # Assume opponent is the other color.
    opponent = "white" if state.current_player == "black" else "black"

    # Check for an immediate winning move for the opponent.
    for move in valid_moves:
        # Simulate opponent move
        simulated_state = state.copy_state()
        if move[0] == "move":
            simulated_state = simulated_state.make_move(move)
            last_move = True
        elif move[0] == "place":
            simulated_state = simulated_state.place_piece(move[1], state.current_player)
            last_move = False
        # Switch turn to opponent for the simulation
        simulated_state.current_player = opponent
        if simulated_state.check_win() == opponent:
            # If opponent can win immediately with this move, then block it.
            return move

    # Otherwise, use epsilon-greedy policy as before:
    if random.random() < EPSILON:
        best_move = None
        best_score = -math.inf if state.current_player == "white" else math.inf
        for move in valid_moves:
            if move[0] == "move":
                new_state = state.make_move(move)
                last = True
            elif move[0] == "place":
                new_state = state.place_piece(move[1], state.current_player)
                last = False
            score = new_state.evaluate_board(last)
            if state.current_player == "white":
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move
    else:
        return random.choice(valid_moves)

def random_playout(state, max_depth, last_play_was_movement):
    current_depth = 0
    current_state = state.copy_state()  # Use your fast copy method
    current_last = last_play_was_movement

    while current_depth < max_depth and not current_state.is_game_over(current_last):
        valid_moves = current_state.get_valid_plays()
        if not valid_moves:
            break

        # Use the safe rollout policy.
        move = safe_rollout_policy(current_state)
        if move is None:
            break

        if move[0] == "move":
            current_state = current_state.make_move(move)
            current_last = True
        elif move[0] == "place":
            current_state = current_state.place_piece(move[1], current_state.current_player)
            current_last = False

        # Switch player.
        current_state.current_player = "white" if current_state.current_player == "black" else "black"
        current_depth += 1

    return current_state.evaluate_board(current_last)

def mcts_search(root_state, iterations=1000, max_depth=20):
    root_node = MCTSNode(root_state)

    for i in range(iterations):
        node = root_node
        state_copy = root_state.copy_state()
        last_play = False

        # Selection
        while node.untried_moves == [] and node.children:
            node = node.uct_select_child()
            if node.move[0] == "move":
                state_copy = state_copy.make_move(node.move)
                last_play = True
            elif node.move[0] == "place":
                state_copy = state_copy.place_piece(node.move[1], state_copy.current_player)
                last_play = False
            state_copy.current_player = "white" if state_copy.current_player == "black" else "black"

        # Expansion
        if node.untried_moves:
            node, last_play = node.expand()
            if node.move[0] == "move":
                state_copy = state_copy.make_move(node.move)
                last_play = True
            elif node.move[0] == "place":
                state_copy = state_copy.place_piece(node.move[1], state_copy.current_player)
                last_play = False
            state_copy.current_player = "white" if state_copy.current_player == "black" else "black"

        # Simulation
        reward = random_playout(state_copy, max_depth, last_play)
        # Backpropagation
        node.update(reward)

    if not root_node.children:
        return None
    best_child = max(root_node.children, key=lambda child: child.visits)
    return best_child.move

# Example usage:
if __name__ == '__main__':
    from GameState import GameState
    initial_state = GameState()
    best_move = mcts_search(initial_state, iterations=500, max_depth=20)
    print("Best move found by MCTS:", best_move)
