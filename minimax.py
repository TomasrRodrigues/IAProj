import copy
from GameState import GameState


def minimax(state, depth, alpha, beta, maximizing_player, last_play, ai_color):
    """Minimax algorithm with alpha-beta pruning for adversarial search.

        Args:
            state: Current GameState object
            depth: Search depth remaining
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: True if current player is maximizing
            last_play: Previous move made
            ai_color: Color of the AI player ('black' or 'white')

        Returns:
            tuple: (best_value, best_move) for current node
        """

    # Base case: depth limit or terminal state
    if depth == 0 or state.is_game_over(last_play):
        # Calculate evaluation score using last play type
        return state.evaluate_board(last_play, ai_color), None

    best_move = None

    if maximizing_player:
        best_value = float('-inf')
        for move in state.get_valid_plays():
            # Generate new state based on move type
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)
            else:
                continue

            # Switch players and store the actual play made
            new_state.current_player = "white" if new_state.current_player == "black" else "black"

            # Recursive call with the actual play as parameter
            value, _ = minimax(new_state, depth - 1, alpha, beta, False, move, ai_color)

            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return best_value, best_move

    else:  # Minimizing player
        best_value = float('inf')
        for move in state.get_valid_plays():
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)
            else:
                continue

            new_state.current_player = "white" if new_state.current_player == "black" else "black"

            value, _ = minimax(new_state, depth - 1, alpha, beta, True, move, ai_color)

            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return best_value, best_move
