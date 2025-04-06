import GameConstants
import copy


width=GameConstants.width

class GameState:
    def __init__(self):
        self.reset()

    #Function to reset the board state (no pieces)
    def reset(self):
        self.pieces = []
        self.reserve = {"black": 6, "white": 6}
        self.current_player = "black"
        self.occupied = set(tile for tile, _ in self.pieces)

    def copy_state(self):
        """
        Create a new GameState with only the mutable parts (pieces, reserve, current_player)
        copied. (Tiles are assumed to be defined globally.)
        """
        new_state = GameState.__new__(GameState)  # create instance without calling __init__
        new_state.pieces = self.pieces.copy()
        new_state.reserve = self.reserve.copy()
        new_state.current_player = self.current_player
        new_state.occupied = self.occupied.copy()
        return new_state

    def place_piece(self, tile, color):
        # Create a deep copy of the current game state
        #new_state = copy.deepcopy(self)

        if tile in self.occupied:
            print("Tile already occupied")
            return self  # Return the unchanged state

        if self.reserve[color] <= 0:
            print(f"No {color} pieces left to place")
            return self  # Return the unchanged state

        # Apply the placement in the new state
        new_state = self.copy_state()
        new_state.pieces.append((tile, color))
        new_state.reserve[color] -= 1
        new_state.occupied.add(tile)

        return new_state  # Return the updated game state

    def make_move(self, move):
        new_state = self.copy_state()

        if type(move[0]) == str:
            _, piece_pos, new_tile = move  # piece_pos is (x, y) instead of an index
        else:
            piece_pos, new_tile = move

        # Find the piece that is currently at piece_pos
        piece_index = None
        for i, (tile, color) in enumerate(new_state.pieces):
            if tile == piece_pos:  # If this piece is at the selected position
                piece_index = i
                break

        if piece_index is None:
            print(f"Error: Piece at position {piece_pos} not found!")
            return self  # Return the unchanged state if there's an error

        # Move the piece
        old_tile, piece_color = self.pieces[piece_index]
        new_state.pieces[piece_index] = (new_tile, piece_color)

        new_state.occupied.discard(old_tile)
        new_state.occupied.add(new_tile)

        # Flip pieces if necessary
        new_state.flip_pieces(new_tile)
        return new_state

    def is_game_over(self, play=None):
        # Always check loss condition (5-in-a-row)
        if self.check_lose() is not None:
            return True

        # Only check win condition for moves
        if play and play[0] == "move":
            return self.check_win(play) is not None

        return False

    def get_valid_plays(self):
        valid_moves = []

        for (piece_pos, piece_color) in self.pieces:
            if piece_color != self.current_player:
                continue
            for dest in self.movable_places(piece_pos, piece_color):
                valid_moves.append(("move", piece_pos, dest))

        if self.reserve[self.current_player] > 0:
            # Precompute all board positions and subtract occupied positions.
            all_tiles = {(i, j) for i in range(1, 6) for j in range(1, 6)}
            available = all_tiles - self.occupied
            for tile in available:
                valid_moves.append(("place", tile))

        return valid_moves

    # BOOLEAN: Check if a tile is occupied
    def is_tile_occupied(self, tile):
        return tile in self.occupied


    # returns a set of the movable places for a piece
    def movable_places(self, piece_pos, piece_color):
        possible_moves = set()
        directions = [
            (0, 1), (0, -1),  # Vertical
            (1, 0), (-1, 0),  # Horizontal
            (1, -1), (-1, 1)  # Diagonal
        ]

        travel_color = "darkblue" if piece_color == "black" else piece_color

        board_tiles = {
            (1, 1): {"color": "grey"}, (1, 2): {"color": "darkblue"},
            (1, 3): {"color": "darkblue"}, (1, 4): {"color": "darkblue"},
            (1, 5): {"color": "grey"}, (2, 1): {"color": "darkblue"},
            (2, 2): {"color": "white"}, (2, 3): {"color": "white"},
            (2, 4): {"color": "white"}, (2, 5): {"color": "darkblue"},
            (3, 1): {"color": "darkblue"}, (3, 2): {"color": "white"},
            (3, 3): {"color": "grey"}, (3, 4): {"color": "white"},
            (3, 5): {"color": "darkblue"}, (4, 1): {"color": "darkblue"},
            (4, 2): {"color": "white"}, (4, 3): {"color": "white"},
            (4, 4): {"color": "white"}, (4, 5): {"color": "darkblue"},
            (5, 1): {"color": "grey"}, (5, 2): {"color": "darkblue"},
            (5, 3): {"color": "darkblue"}, (5, 4): {"color": "darkblue"},
            (5, 5): {"color": "grey"}
        }

        for dx, dy in directions:
            x, y = piece_pos
            while True:
                x += dx
                y += dy
                if not (1 <= x <= 5 and 1 <= y <= 5):
                    break
                if self.is_tile_occupied((x, y)):
                    break
                # If the tile is not of the travel color, you can only move one step.
                if board_tiles[(x, y)]["color"] != travel_color:
                    possible_moves.add((x, y))
                    break
                possible_moves.add((x, y))

        return possible_moves


    def is_valid_move(self, original_position, expected_position):
        for move in self.movable_places(original_position, self.get_piece_at(original_position)[1]):
            if move == expected_position:
                return True
        return False


    def flip_pieces(self, moved_to):
        directions = [
            (0, 1), (0, -1),  # Vertical
            (1, 0), (-1, 0),  # Horizontal
            (1, -1), (-1, 1)  # Diagonal
        ]

        opponent = "white" if self.current_player=="black" else "black"

        for dx, dy in directions:
            x, y = moved_to
            to_flip = []
            while True:
                x += dx
                y += dy
                if not (1 <= x <= 5 and 1 <= y <= 5):
                    break
                # Check if there is a piece at (x, y)
                piece = self.get_piece_at((x, y))
                if piece is None:
                    break
                if piece[1] == opponent:
                    to_flip.append((x, y))
                elif piece[1] == self.current_player:
                    # Flip all opponent pieces in between
                    for flip_tile in to_flip:
                        # Find index of piece at flip_tile and flip its color
                        for idx, (tile, col) in enumerate(self.pieces):
                            if tile == flip_tile:
                                self.pieces[idx] = (tile, self.current_player)
                                break
                    break
                else:
                    break


    def get_piece_at(self, tile):
        for piece in self.pieces:
            if piece[0] == tile:
                return piece
        return None


    # Check lose function
    def check_lose(self):
        directions = [
            (0, 1),  # Vertical
            (1, 0),  # Horizontal
            (1, -1)  # Diagonal
        ]
        for (pos, color) in self.pieces:
            if pos == (-1, -1):
                continue
            for dx, dy in directions:
                count = 1
                x, y = pos
                while True:
                    x += dx
                    y += dy
                    if 1 <= x <= 5 and 1 <= y <= 5 and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                x, y = pos
                while True:
                    x -= dx
                    y -= dy
                    if 1 <= x <= 5 and 1 <= y <= 5 and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                if count >= 5:
                    return color
        return None

    # Check win does not check if the play was a movement, yet to implement
    def check_win(self, play=None):
        """Check if the SPECIFIC MOVE created a 4-in-a-row."""
        if not play or play[0] != "move":
            return None  # Only check moves, not placements

        # Get moved piece's final position and color
        _, initial_pos, dest_pos = play
        color = self.get_piece_at(dest_pos)[1]

        directions = [(0, 1), (1, 0), (1, -1)]  # Vertical, Horizontal, Diagonal

        for dx, dy in directions:
            count = 1
            x, y = dest_pos

            # Check in positive direction
            while True:
                x += dx
                y += dy
                if (1 <= x <= 5 and 1 <= y <= 5 and
                        any(p[0] == (x, y) and p[1] == color for p in self.pieces)):
                    count += 1
                else:
                    break

            # Check in negative direction
            x, y = dest_pos
            while True:
                x -= dx
                y -= dy
                if (1 <= x <= 5 and 1 <= y <= 5 and
                        any(p[0] == (x, y) and p[1] == color for p in self.pieces)):
                    count += 1
                else:
                    break

            if count == 4:
                return color
        return None


    def evaluate_board(self, play, ai_color):
        ai_opponent = "black" if ai_color == "white" else "white"

        # Immediate loss/win conditions
        lose_result = self.check_lose()
        #if lose_result == ai_color:
        #    return -10000
        #elif lose_result == ai_opponent:
        #    return 10000
        if lose_result is not None:
            return -10000

        # Check for win conditions (only after a movement)
        if play and play[0] == "move":
            win_result = self.check_win(play)
            if win_result == ai_color:
                return 9000
            elif win_result == ai_opponent:
                return -9000

        score = 0

        # Threat detection: opponent's 3+ alignment
        for (pos, color) in self.pieces:
            if color == ai_opponent:
                align = self.count_alignment(pos, ai_opponent)
                if align >= 3:
                    score -= 1000

        # Alignment scoring
        for (pos, color) in self.pieces:
            align = self.count_alignment(pos, color)
            if color == ai_color:
                score += align * 10
            else:
                score -= align * 15

        # Mobility: compare AI's and opponent's valid moves
        temp_ai_state = self.copy_state()
        temp_ai_state.current_player = ai_color
        ai_moves = len(temp_ai_state.get_valid_plays())

        temp_opponent_state = self.copy_state()
        temp_opponent_state.current_player = ai_opponent
        opponent_moves = len(temp_opponent_state.get_valid_plays())

        score += (ai_moves - opponent_moves) * 5

        return score


    def count_alignment(self, position, player):
        directions = [(0, 1), (1, 0), (1, -1)]
        total = 0
        for dx, dy in directions:
            count = 1
            x, y = position

            # Check positive direction
            while True:
                x += dx
                y += dy
                if not (1 <= x <= 5 and 1 <= y <= 5):
                    break
                if any(p[0] == (x, y) and p[1] == player for p in self.pieces):
                    count += 1
                else:
                    break

            # Check negative direction
            x, y = position
            while True:
                x -= dx
                y -= dy
                if not (1 <= x <= 5 and 1 <= y <= 5):
                    break
                if any(p[0] == (x, y) and p[1] == player for p in self.pieces):
                    count += 1
                else:
                    break

            if count == 3:
                total += 5
            elif count == 2:
                total += 2
        return total

