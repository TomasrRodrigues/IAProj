# montecarlo.py
import math
import random
import copy

UCT_CONSTANT = 1.414
EPSILON = 0.2

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

def rollout_policy(state, ai_color):
    valid_moves = state.get_valid_plays()
    if not valid_moves:
        return None
    if random.random() < EPSILON:
        best_move = None
        best_score = -math.inf
        for move in valid_moves:
            if move[0] == "move":
                new_state = state.make_move(move)
                last = True
            elif move[0] == "place":
                new_state = state.place_piece(move[1], state.current_player)
                last = False
            score = new_state.evaluate_board(last, ai_color)
            if state.current_player == ai_color:
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


def safe_rollout_policy(state, ai_color):
    valid_moves = state.get_valid_plays()
    if not valid_moves:
        return None

    opponent = "black" if ai_color == "white" else "white"

    # Check if any move allows opponent to win next turn
    for move in valid_moves:
        simulated_state = state.copy_state()

        # Apply current player's move
        if move[0] == "move":
            simulated_state = simulated_state.make_move(move)
        elif move[0] == "place":
            simulated_state = simulated_state.place_piece(move[1], state.current_player)

        # Check opponent's possible responses
        simulated_state.current_player = opponent
        if simulated_state.check_win() == opponent and move[0] == "move":
            return move  # Block dangerous moves that let opponent win

        # Check if opponent can win immediately
        for opp_move in simulated_state.get_valid_plays():
            temp_state = simulated_state.copy_state()
            if opp_move[0] == "move":
                temp_state = temp_state.make_move(opp_move)
                if temp_state.check_win() == opponent:
                    return move  # Block this move

    # Epsilon-greedy fallback
    if random.random() < EPSILON:
        best_move = None
        best_score = -math.inf
        for move in valid_moves:
            if move[0] == "move":
                new_state = state.make_move(move)
                last = True
            elif move[0] == "place":
                new_state = state.place_piece(move[1], state.current_player)
                last = False
            score = new_state.evaluate_board(last, ai_color)
            if state.current_player == ai_color and score > best_score:
                best_score = score
                best_move = move
            elif state.current_player != ai_color and score < best_score:
                best_score = score
                best_move = move
        return best_move
    else:
        return random.choice(valid_moves)


def random_playout(state, max_depth, last_play_was_movement, ai_color):
    current_depth = 0
    current_state = state.copy_state()
    current_last = last_play_was_movement
    opponent_color = "black" if ai_color == "white" else "white"

    while current_depth < max_depth:
        # Check for immediate loss/win conditions
        loser = current_state.check_lose()
        if loser == ai_color:
            return -10000  # AI loses
        elif loser == opponent_color:
            return 10000  # Opponent loses

        if current_last:  # Check win only after movements
            winner = current_state.check_win()
            if winner == ai_color:
                return 9000
            elif winner == opponent_color:
                return -9000

        valid_moves = current_state.get_valid_plays()
        if not valid_moves:
            break

        move = safe_rollout_policy(current_state, ai_color)
        if move is None:
            break

        # Apply the move
        if move[0] == "move":
            current_state = current_state.make_move(move)
            current_last = True
        else:
            current_state = current_state.place_piece(move[1], current_state.current_player)
            current_last = False

        current_state.current_player = "white" if current_state.current_player == "black" else "black"
        current_depth += 1

    return current_state.evaluate_board(current_last, ai_color)


def mcts_search(root_state, iterations=1000, max_depth=20, ai_color="white"):
    root_node = MCTSNode(root_state)
    opponent_color = "black" if ai_color == "white" else "white"

    for _ in range(iterations):
        node = root_node
        state_copy = root_state.copy_state()
        last_play = False
        terminal = False

        # Selection phase
        while not terminal and node.untried_moves == [] and node.children:
            node = node.uct_select_child()
            # Apply the move to our state copy
            if node.move[0] == "move":
                state_copy = state_copy.make_move(node.move)
                last_play = True
            elif node.move[0] == "place":
                state_copy = state_copy.place_piece(node.move[1], state_copy.current_player)
                last_play = False

            # Immediately check for terminal states
            if state_copy.check_lose() == ai_color:
                reward = -10000  # Immediate loss
                node.update(reward)
                terminal = True
            elif state_copy.check_lose() == opponent_color:
                reward = 10000  # Immediate win
                node.update(reward)
                terminal = True

            state_copy.current_player = opponent_color if state_copy.current_player == ai_color else ai_color

        if terminal:
            continue  # Skip expansion/simulation for terminal nodes

        # Expansion phase
        if node.untried_moves:
            move = node.untried_moves.pop()
            if move[0] == "move":
                new_state = node.state.make_move(move)
                last_play = True
            else:
                new_state = node.state.place_piece(move[1], node.state.current_player)
                last_play = False

            # Create child node
            child_state = new_state.copy_state()
            child_state.current_player = opponent_color if node.state.current_player == ai_color else ai_color
            child_node = MCTSNode(child_state, parent=node, move=move)
            node.children.append(child_node)
            node = child_node

            # Update state copy to match new node
            state_copy = child_state.copy_state()

        # Simulation phase with early termination checks
        reward = 0
        if not terminal:
            sim_state = state_copy.copy_state()
            current_depth = 0
            sim_last = last_play

            while current_depth < max_depth:
                # Check for immediate loss/win
                loser = sim_state.check_lose()
                if loser == ai_color:
                    reward = -10000
                    break
                elif loser == opponent_color:
                    reward = 10000
                    break

                if sim_last:  # Win checks only after movements
                    winner = sim_state.check_win()
                    if winner == ai_color:
                        reward = 9000
                        break
                    elif winner == opponent_color:
                        reward = -9000
                        break

                # Get valid moves
                valid_moves = sim_state.get_valid_plays()
                if not valid_moves:
                    break

                # Select move using safe policy
                move = safe_rollout_policy(sim_state, ai_color)
                if not move:
                    break

                # Apply move
                if move[0] == "move":
                    sim_state = sim_state.make_move(move)
                    sim_last = True
                else:
                    sim_state = sim_state.place_piece(move[1], sim_state.current_player)
                    sim_last = False

                # Switch players
                sim_state.current_player = opponent_color if sim_state.current_player == ai_color else ai_color
                current_depth += 1

            # If no terminal state found, use evaluation
            if reward == 0:
                reward = sim_state.evaluate_board(sim_last, ai_color)

        # Backpropagation with loss protection
        node.update(reward)

    # Select move with highest visit count that doesn't lead to immediate loss
    best_child = None
    best_score = -float('inf')
    for child in root_node.children:
        # Penalize moves that lead to certain loss
        loss_penalty = 0
        if child.state.check_lose() == ai_color:
            loss_penalty = -1000000

        child_score = (child.total_reward / child.visits) + loss_penalty
        if child_score > best_score:
            best_score = child_score
            best_child = child

    return best_child.move if best_child else None

# Example usage remains the same