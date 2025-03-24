from game import isTerminal, evaluate_board, get_valid_moves, make_move, check_win, check_lose
import copy

def isTerminal(board_state, original_position):
    if check_win(original_position) is not None or check_lose() is not None:
        return True
    return False


def make_move(board_state, move):
    new_board = copy.deepcopy(board_state)
    piece_index, new_tile = move
    piece = new_board[piece_index]
    original_position = piece[0]
    new_board[piece_index] = (new_tile, piece[1])

    new_board = flip_pieces_on_board(new_board, new_tile, original_position, piece[1])
    return new_board

def flip_pieces_on_board(board, moved_to, original_position, player_color):
    """
    Similar to your flip_pieces but operating on the provided board state.
    Returns the board after flipping opponent pieces.
    """
    directions = [
        (0, 1), (0, -1),
        (1, 0), (-1, 0),
        (1, -1), (-1, 1)
    ]
    if original_position == (-1, -1):
        return board  # No flipping when placing a piece from reserve
    opponent_color = "white" if player_color == "black" else "black"
    for dx, dy in directions:
        x, y = moved_to
        to_flip = []
        while True:
            x += dx
            y += dy
            if (x, y) not in tiles:
                break
            found_piece = None
            for i, piece in enumerate(board):
                if piece[0] == (x, y):
                    found_piece = (i, piece[1])
                    break
            if found_piece is None:
                break
            if found_piece[1] == opponent_color:
                to_flip.append(found_piece[0])
            elif found_piece[1] == player_color:
                for idx in to_flip:
                    # Flip the piece by simply setting its color to player_color.
                    board[idx] = (board[idx][0], player_color)
                break
            else:
                break
    return board

def minimax(board_state, depth, alpha, beta, maximizingPlayer, player_color, original_position):

    if depth ==0 or isTerminal(board_state, original_position):
        return evaluate_board(board_state, player_color, original_position), None

    if maximizingPlayer:
        maxEval = float("-inf")
        bestMove = None
        for move in get_valid_moves(board_state, player_color):
            new_board_state = make_move(board_state, move)
            eval, _ = minimax(new_board_state, depth - 1, alpha, beta, False, player_color, move[1])
            if eval > maxEval:
                maxEval = eval
                bestMove = move
            alpha= max(alpha, eval)
            if alpha >= beta:
                break
        return maxEval, bestMove

    else:
        opponent = "white" if player_color=="black" else "black"
        bestScore=float("inf")
        bestMove=None
        for move in get_valid_moves(board_state, opponent):
            new_board_state= make_move(board_state, move)
            score, _ = minimax(new_board_state, depth - 1, alpha, beta, True, player_color, move[1])
            if score < bestScore:
                bestScore = score
                bestMove = move
            beta= min(beta, score)
            if alpha >= beta:
                break
        return bestScore, bestMove