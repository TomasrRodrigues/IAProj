def minimax(state, depth, alpha, beta, maximizing_player, last_play_was_movement):
    """
    Minimax algorithm with Alpha-Beta Pruning.

    - `state`: The current game state.
    - `depth`: The remaining depth to search.
    - `alpha`: Best already found for maximizing player.
    - `beta`: Best already found for minimizing player.
    - `maximizing_player`: True if it's AI's turn, False if it's the opponent's.
    - `last_play_was_movement`: True if last action was a move, False if it was a placement.
    """

    # Base case: If depth is 0 or the game is over, evaluate the board
    if depth == 0 or state.is_game_over(last_play_was_movement):
        return state.evaluate_board(last_play_was_movement), None  # Return board evaluation

    best_move = None

    if maximizing_player:
        best_value = float('-inf')
        for move in state.get_valid_plays():
            print(move)
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)

            # Update last_play_was_movement flag
            new_last_play_was_movement = (move[0] == "move")

            # Recursively call minimax for the opponent's turn
            value, _ = minimax(new_state, depth - 1, alpha, beta, False, new_last_play_was_movement)

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)
            if beta <= alpha:  # Beta cutoff
                break
    else:
        best_value = float('inf')
        for move in state.get_valid_plays():
            print(move)
            if move[0] == 'move':
                new_state = state.make_move(move)
            elif move[0] == 'place':
                new_state = state.place_piece(move[1], state.current_player)

            # Update last_play_was_movement flag
            new_last_play_was_movement = (move[0] == "move")

            # Recursively call minimax for the opponent's turn
            value, _ = minimax(new_state, depth - 1, alpha, beta, True, new_last_play_was_movement)

            if value < best_value:
                best_value = value
                best_move = move

            beta = min(beta, best_value)
            if beta <= alpha:  # Alpha cutoff
                break

    return best_value, best_move
