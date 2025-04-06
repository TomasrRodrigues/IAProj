import math
import random
from GameState import GameState

class MCTSNode:
    def __init__(self, state, move=None, parent=None, last_move=None):
        self.state = state                # The game state at this node.
        self.move = move                  # The move that led to this state.
        self.parent = parent              # Parent node.
        self.last_move = last_move        # Last move applied to reach this state.
        self.children = []
        self.visits = 0
        self.total_reward = 0.0
        self.untried_moves = state.get_valid_plays()  # All valid moves from this state.

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=math.sqrt(2)):
        # UCT selection: exploitation + exploration term.
        choices_weights = [
            (child.total_reward / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        # Choose a random move from the untried moves.
        move = self.untried_moves.pop(random.randrange(len(self.untried_moves)))
        new_state = self.state.copy_state()

        # Apply the move.
        if move[0] == 'move':
            new_state = new_state.make_move(move)
        elif move[0] == 'place':
            new_state = new_state.place_piece(move[1], new_state.current_player)

        # Switch player after move application.
        new_state.current_player = "white" if new_state.current_player == "black" else "black"

        # Create a new node with the move stored as the last move.
        child_node = MCTSNode(new_state, move=move, parent=self, last_move=move)
        self.children.append(child_node)
        return child_node

    def update(self, reward):
        self.visits += 1
        self.total_reward += reward

def choose_move(state, ai_color):
    """
    Choose a move using a heuristic that:
      - If enough pieces are on the board (>= 4), first checks for immediate winning or blocking moves.
      - Otherwise, or if no immediate moves exist, uses an evaluation function:
        - If it's the AI's turn, chooses the move with the highest evaluation.
        - If it's the opponent's turn, chooses the move with the lowest evaluation.
    """
    valid_moves = state.get_valid_plays()
    if not valid_moves:
        return None

    # Only check for immediate wins/blocks if enough pieces are on board.
    if len(state.pieces) >= 4:
        for move in valid_moves:
            new_state = state.copy_state()
            if move[0] == 'move':
                new_state = new_state.make_move(move)
            elif move[0] == 'place':
                new_state = new_state.place_piece(move[1], new_state.current_player)
            # If the move ends the game immediately...
            if new_state.is_game_over(move):
                # If it wins for the AI, take it.
                if new_state.check_win(move) == ai_color:
                    return move
                # Or, if the move prevents an immediate opponent win, choose it.
                elif new_state.check_win(move) is not None:
                    return move

    # Fall back to a heuristic evaluation if no immediate win/block is found or if board is too empty.
    if state.current_player == ai_color:
        best_move = None
        best_score = -float('inf')
        for move in valid_moves:
            new_state = state.copy_state()
            if move[0] == 'move':
                new_state = new_state.make_move(move)
            elif move[0] == 'place':
                new_state = new_state.place_piece(move[1], new_state.current_player)
            new_state.current_player = "white" if new_state.current_player == "black" else "black"
            score = new_state.evaluate_board(move, ai_color)
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_move = None
        best_score = float('inf')
        for move in valid_moves:
            new_state = state.copy_state()
            if move[0] == 'move':
                new_state = new_state.make_move(move)
            elif move[0] == 'place':
                new_state = new_state.place_piece(move[1], new_state.current_player)
            new_state.current_player = "white" if new_state.current_player == "black" else "black"
            score = new_state.evaluate_board(move, ai_color)
            if score < best_score:
                best_score = score
                best_move = move

    return best_move if best_move is not None else random.choice(valid_moves)

def heuristic_rollout(state, rollout_depth, ai_color, last_move=None):
    """
    Run a rollout using a heuristic rollout policy.
    At each step, if an immediate win is available for either side and enough pieces are on board,
    it is taken. Otherwise, choose_move is used.
    """
    current_state = state.copy_state()
    rollout_last_move = last_move

    for _ in range(rollout_depth):
        if current_state.is_game_over(rollout_last_move):
            break

        valid_moves = current_state.get_valid_plays()
        if not valid_moves:
            break

        move = choose_move(current_state, ai_color)
        rollout_last_move = move

        if move[0] == 'move':
            current_state = current_state.make_move(move)
        elif move[0] == 'place':
            current_state = current_state.place_piece(move[1], current_state.current_player)

        current_state.current_player = "white" if current_state.current_player == "black" else "black"

    return current_state.evaluate_board(rollout_last_move, ai_color)

def montecarlo(state, num_simulations, rollout_depth, ai_color):
    """
    Perform Monte Carlo Tree Search starting from 'state' using num_simulations and
    rollouts of depth 'rollout_depth'. The ai_color parameter is used in evaluation.
    """
    root_node = MCTSNode(state, last_move=None)

    for _ in range(num_simulations):
        node = root_node

        # Selection: traverse using best_child until reaching a node that is not fully expanded.
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # Expansion: expand the node if it's not fully expanded.
        if not node.is_fully_expanded():
            node = node.expand()

        # Simulation: perform a heuristic rollout from the node's state.
        reward = heuristic_rollout(node.state, rollout_depth, ai_color, last_move=node.last_move)

        # Backpropagation: update the node and its ancestors with the simulation result.
        while node is not None:
            node.update(reward)
            node = node.parent

    best_move = max(root_node.children, key=lambda child: child.visits).move
    return best_move
