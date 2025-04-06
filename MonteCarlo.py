import math
import random
from GameState import GameState


class MCTSNode:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_reward = 0.0
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
        move = self.untried_moves.pop(random.randrange(len(self.untried_moves)))
        new_state = self.state.copy_state()

        # Apply move
        if move[0] == 'move':
            new_state = new_state.make_move(move)
        elif move[0] == 'place':
            new_state = new_state.place_piece(move[1], new_state.current_player)

        # Switch player AFTER move is completed
        new_state.current_player = "white" if new_state.current_player == "black" else "black"
        child_node = MCTSNode(new_state, move=move, parent=self)
        self.children.append(child_node)
        return child_node

    def update(self, reward):
        self.visits += 1
        self.total_reward += reward


def rollout_policy(state, ai_color):
    valid_moves = state.get_valid_plays()
    best_move = None
    best_score = -float('inf')
    opponent = "black" if ai_color == "white" else "white"

    for move in valid_moves:
        # Simulate current move
        new_state = state.copy_state()
        if move[0] == 'move':
            new_state = new_state.make_move(move)
        elif move[0] == 'place':
            new_state = new_state.place_piece(move[1], state.current_player)

        # Immediate win check
        if new_state.is_game_over(move):
            win_result = new_state.check_win(move)
            lose_result = new_state.check_lose()
            if win_result == ai_color or lose_result == opponent:
                return move  # Immediate best move found

        # Opponent response simulation
        new_state.current_player = opponent
        opp_has_winning_move = False

        for opp_move in new_state.get_valid_plays():
            opp_state = new_state.copy_state()
            if opp_move[0] == 'move':
                opp_state = opp_state.make_move(opp_move)
            elif opp_move[0] == 'place':
                opp_state = opp_state.place_piece(opp_move[1], opp_state.current_player)

            if opp_state.is_game_over(opp_move):
                opp_win = opp_state.check_win(opp_move)
                opp_lose = opp_state.check_lose()
                if opp_win == opponent or opp_lose == ai_color:
                    opp_has_winning_move = True
                    break

        # Scoring logic
        if opp_has_winning_move:
            score = -100000  # Catastrophic score for allowing opponent win
        else:
            score = new_state.evaluate_board(move, ai_color)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move if best_move else random.choice(valid_moves)


def simulate_rollout(state, rollout_depth, ai_color):
    current_state = state.copy_state()
    last_move = None
    for _ in range(rollout_depth):
        if current_state.is_game_over(last_move):
            break
        move = rollout_policy(current_state, ai_color)
        last_move = move

        # Apply move
        if move[0] == 'move':
            current_state = current_state.make_move(move)
        elif move[0] == 'place':
            current_state = current_state.place_piece(move[1], current_state.current_player)

        # Switch player
        current_state.current_player = "white" if current_state.current_player == "black" else "black"

    return current_state.evaluate_board(last_move, ai_color)


def montecarlo(state, num_simulations, depth, ai_color):
    root_node = MCTSNode(state)

    for _ in range(num_simulations):
        node = root_node

        # Selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # Expansion
        if not node.is_fully_expanded():
            node = node.expand()

        # Simulation
        reward = simulate_rollout(node.state, depth, ai_color)

        # Backpropagation
        while node is not None:
            node.update(reward)
            node = node.parent

    # Select most visited child
    return max(root_node.children, key=lambda child: child.visits).move