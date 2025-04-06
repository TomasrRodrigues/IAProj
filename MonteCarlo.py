import math
import random
from GameState import GameState

class MCTSNode:
    """Represents a node in the MCTS (Monte Carlo Tree Search)"""
    def __init__(self, state, move=None, parent=None, last_move=None):
        """Initialize MCTS node with game state and metadata

        Args:
            state: Current game state
            move: Move that led to this state
            parent: Parent node in MCTS tree
            last_move: Last move that led to this state
        """
        self.state = state                # The game state at this node.
        self.move = move                  # The move that led to this state.
        self.parent = parent              # Parent node.
        self.last_move = last_move        # Last move applied to reach this state.
        self.children = []
        self.visits = 0
        self.total_reward = 0.0
        self.untried_moves = state.get_valid_plays()  # All valid moves from this state.

    def is_fully_expanded(self):
        """Check if all possible moves have been explored from this node."""
        return len(self.untried_moves) == 0

    def best_child(self, c_param=math.sqrt(2)):
        """Select child node using Upper Confidence Bound for Trees (UCT) formula.

                Balances exploitation (high reward) vs exploration (under-visited nodes)
                """
        choices_weights = [
            (child.total_reward / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        """Create new child node by trying an unexplored move."""
        #select random untried move
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
        """Update node statistics after simulation."""
        self.visits += 1
        self.total_reward += reward

def choose_move(state, ai_color):
    """Select move using heuristic strategy combining immediate win checks and evaluation.

    Strategy:
    1. Check for immediate winning/blocking moves when board has >=4 pieces
    2. Fallback to evaluation function for other cases:
       - Maximizes score for AI player
       - Minimizes score for opponent
    """
    valid_moves = state.get_valid_plays()
    if not valid_moves:
        return None

    # Immediate win/block check
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

    #Heuristic evaluation fallback
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
    """Simulate game from current state using heuristic policy.

    Args:
        state: Starting game state
        rollout_depth: Maximum moves to simulate
        ai_color: AI's color for evaluation
        last_move: Move that led to current state

    Returns:
        Final heuristic evaluation of simulated game state
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
    """Execute Monte Carlo Tree Search algorithm.

    Process:
    1. Selection: Traverse tree using UCT
    2. Expansion: Add new node if possible
    3. Simulation: Rollout game from expanded node
    4. Backpropagation: Update node statistics

    Returns:
        Best move found through MCTS process
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
