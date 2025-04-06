import math
import random
import copy
from GameState import GameState


class MCTSNode:
    def __init__(self, state, move=None, parent=None):
        self.state = state  # GameState at this node
        self.move = move  # The move that led to this state (None for the root)
        self.parent = parent  # Parent node (None for the root)
        self.children = []  # Child nodes
        self.visits = 0  # Number of times the node was visited
        self.total_reward = 0.0  # Cumulative reward from rollouts
        # All valid moves from the current state, to be tried during expansion.
        self.untried_moves = state.get_valid_plays()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=math.sqrt(2)):
        # Use UCT: average reward plus an exploration bonus.
        choices_weights = [
            (child.total_reward / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        # Select and remove an untried move randomly.
        move = self.untried_moves.pop(random.randrange(len(self.untried_moves)))
        new_state = self.state.copy_state()
        if move[0] == 'move':
            new_state = new_state.make_move(move)
        elif move[0] == 'place':
            new_state = new_state.place_piece(move[1], new_state.current_player)
        # Switch the current player.
        new_state.current_player = "white" if new_state.current_player == "black" else "black"
        child_node = MCTSNode(new_state, move=move, parent=self)
        self.children.append(child_node)
        return child_node

    def update(self, reward):
        self.visits += 1
        self.total_reward += reward


def rollout_policy(state, ai_color):
    """
    Heuristic rollout policy that examines all valid moves and chooses
    the one that produces the best immediate evaluation for the current state.
    This bias helps in blocking clear winning moves by the opponent.
    """
    valid_moves = state.get_valid_plays()
    best_move = None
    best_score = -float('inf')
    for move in valid_moves:
        # Copy the state and apply the move.
        new_state = state.copy_state()
        if move[0] == 'move':
            new_state = new_state.make_move(move)
        elif move[0] == 'place':
            new_state = new_state.place_piece(move[1], state.current_player)
        # Switch the player for the next turn.
        new_state.current_player = "white" if state.current_player == "black" else "black"
        # Evaluate the resulting state.
        score = new_state.evaluate_board(move, ai_color)
        if score > best_score:
            best_score = score
            best_move = move
    if best_move is None:
        best_move = random.choice(valid_moves)
    return best_move


def simulate_rollout(state, rollout_depth, ai_color):
    """
    Simulate a playout (rollout) from the given state using a heuristic rollout
    policy instead of purely random moves. This rollout goes for a maximum of
    rollout_depth moves or stops early if the game ends.
    """
    current_state = state.copy_state()
    last_move = None
    for _ in range(rollout_depth):
        if current_state.is_game_over(last_move):
            break
        valid_moves = current_state.get_valid_plays()
        if not valid_moves:
            break
        # Use the heuristic rollout policy to pick a move.
        move = rollout_policy(current_state, ai_color)
        last_move = move
        if move[0] == 'move':
            current_state = current_state.make_move(move)
        elif move[0] == 'place':
            current_state = current_state.place_piece(move[1], current_state.current_player)
        # Switch the current player.
        current_state.current_player = "white" if current_state.current_player == "black" else "black"
    return current_state.evaluate_board(last_move, ai_color)


def montecarlo(state, num_simulations, depth, ai_color):
    """
    Run Monte Carlo Tree Search starting from root_state.

    Parameters:
      state (GameState): The starting state of the game.
      num_simulations (int): Number of iterations (simulations) to run.
      depth (int): Maximum moves to simulate in each rollout.
      ai_color (str): The AI's color ("black" or "white") for evaluation.

    Returns:
      The best move from the root state's valid plays.
    """
    root_node = MCTSNode(state)

    for _ in range(num_simulations):
        node = root_node
        # SELECTION: Traverse the tree using UCT until reaching a node that is not fully expanded.
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # EXPANSION: Expand the node if it's not fully expanded.
        if not node.is_fully_expanded():
            node = node.expand()

        # SIMULATION: Run a rollout from the newly expanded node.
        reward = simulate_rollout(node.state, depth, ai_color)

        # BACKPROPAGATION: Propagate the reward up the tree.
        while node is not None:
            node.update(reward)
            node = node.parent

    # Select the move from the root that was visited the most.
    best_move = None
    best_visits = -1
    for child in root_node.children:
        if child.visits > best_visits:
            best_visits = child.visits
            best_move = child.move
    return best_move

# Example usage:
# Assuming 'state' is an instance of GameState and your AI plays as "black":
# best_move = monte_carlo_tree_search(state, iterations=1000, rollout_depth=10, ai_color="black")
# print("MCTS selected move:", best_move)
