import copy
from GameState import GameState


def minimax(state, depth, alpha, beta, maximizing_player, last_play_was_movement):
    """
    Minimax algorithm with alpha–beta pruning.

    Parameters:
      - state: the current GameState instance.
      - depth: remaining depth to search.
      - alpha: best value found so far for the maximizing side.
      - beta: best value found so far for the minimizing side.
      - maximizing_player: True if it is the maximizing player's turn.
      - last_play_was_movement: True if the previous action was a move (which can trigger win checking).

    Returns:
      A tuple (evaluation, best_move), where best_move is one of the valid plays.
    """

    # Base case: if depth is 0 or the game is over, evaluate the board.
    if depth == 0 or state.is_game_over(last_play_was_movement):
        return state.evaluate_board(last_play_was_movement), None

    best_move = None

    if maximizing_player:
        best_value = float('-inf')
        for move in state.get_valid_plays():
            # For each valid play, generate a new state.
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)
            else:
                continue

            new_state.current_player = "white" if new_state.current_player=="black" else "black"

            # Update the flag: a move sets it True, a placement sets it False.
            new_last = (move[0] == 'move')

            # Recurse: the next turn is for the minimizing player.
            value, _ = minimax(new_state, depth - 1, alpha, beta, False, new_last)

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Beta cutoff.
        return best_value, best_move

    else:  # Minimizing player's turn.
        best_value = float('inf')
        for move in state.get_valid_plays():
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)
            else:
                continue

            new_last = (move[0] == 'move')
            new_state.current_player = "white" if new_state.current_player=="black" else "black"
            value, _ = minimax(new_state, depth - 1, alpha, beta, True, new_last)

            if value < best_value:
                best_value = value
                best_move = move

            beta = min(beta, best_value)
            if beta <= alpha:
                break  # Alpha cutoff.
        return best_value, best_move
