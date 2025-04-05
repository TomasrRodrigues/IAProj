import copy
from GameState import GameState


def minimax(state, depth, alpha, beta, maximizing_player, last_play_was_movement, ai_color):
    if depth == 0 or state.is_game_over(last_play_was_movement):
        return state.evaluate_board(last_play_was_movement, ai_color), None

    best_move = None

    if maximizing_player:
        best_value = float('-inf')
        for move in state.get_valid_plays():
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)
            else:
                continue

            new_state.current_player = "white" if new_state.current_player == "black" else "black"
            new_last = (move[0] == 'move')

            value, _ = minimax(new_state, depth-1, alpha, beta, False, new_last, ai_color)

            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move

    else:
        best_value = float('inf')
        for move in state.get_valid_plays():
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)
            else:
                continue

            new_state.current_player = "white" if new_state.current_player == "black" else "black"
            new_last = (move[0] == 'move')

            value, _ = minimax(new_state, depth-1, alpha, beta, True, new_last, ai_color)

            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move
