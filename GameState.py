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


    def place_piece(self, tile, color):
        # Create a deep copy of the current game state
        new_state = copy.deepcopy(self)

        if new_state.is_tile_occupied(tile):
            print("Tile already occupied")
            return self  # Return the unchanged state

        if new_state.reserve[color] <= 0:
            print(f"No {color} pieces left to place")
            return self  # Return the unchanged state

        # Apply the placement in the new state
        new_state.pieces.append((tile, color))
        new_state.reserve[color] -= 1

        return new_state  # Return the updated game state

    def make_move(self, move):
        new_state = copy.deepcopy(self)

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
        new_state.pieces[piece_index] = (new_tile, new_state.pieces[piece_index][1])

        # Flip pieces if necessary
        new_state.flip_pieces(new_tile)

        return new_state

    def is_game_over(self, last_play_was_movement):
        """
        Returns True if the game has ended based on the last action.

        A player loses immediately after either a move or a placement.
        A player wins only after a move.
        """
        if self.check_lose() is not None:  # If someone lost, the game is over
            return True
        if last_play_was_movement and self.check_win() is not None:  # Winning only happens after a move
            return True
        return False

    def get_valid_plays(self):
        valid_moves = []

        #Get Valid moves
        print(self.pieces)
        for piece_pos, piece_color in self.pieces:
            if piece_color!=self.current_player:
                continue
            moves= self.movable_places(piece_pos, piece_color)
            for move in moves:
                valid_moves.append(("move", piece_pos, move))

        #Get Valid places
        if self.reserve[self.current_player]>0:
            #for tile in tiles:
            for i in range(1,6):
                for j in range(1,6):
                    if not self.is_tile_occupied((i, j)):
                        valid_moves.append(("place", (i, j)))

        return valid_moves

    # BOOLEAN: Check if a tile is occupied
    def is_tile_occupied(self, tile):
        for piece in self.pieces:
            if piece[0] == tile:
                return True
        return False

    #vasv
        # returns a set of the movable places for a piece
    def movable_places(self, piece_pos, piece_color):
        possible_moves = set()

        directions = [
            (0, 1), (0, -1),  # Vertical
            (1, 0), (-1, 0),  # Horizontal
            (1, -1), (-1, 1)  # Diagonal
        ]

        tiles = {
            (1, 1): {"color": "grey", "pos": (-3 * width, 0)},
            (1, 2): {"color": "darkblue", "pos": (-9 / 4 * width, -width / 2)},
            (1, 3): {"color": "darkblue", "pos": (-3 / 2 * width, -width)},
            (1, 4): {"color": "darkblue", "pos": (-3 / 4 * width, -3 / 2 * width)},
            (1, 5): {"color": "grey", "pos": (0, -2 * width)},
            (2, 1): {"color": "darkblue", "pos": (-9 / 4 * width, width / 2)},
            (2, 2): {"color": "white", "pos": (-3 / 2 * width, 0)},
            (2, 3): {"color": "white", "pos": (-3 / 4 * width, -width / 2)},
            (2, 4): {"color": "white", "pos": (0, -width)},
            (2, 5): {"color": "darkblue", "pos": (3 / 4 * width, -3 / 2 * width)},
            (3, 1): {"color": "darkblue", "pos": (-3 / 2 * width, width)},
            (3, 2): {"color": "white", "pos": (-3 / 4 * width, width / 2)},
            (3, 3): {"color": "grey", "pos": (0, 0)},
            (3, 4): {"color": "white", "pos": (3 / 4 * width, -width / 2)},
            (3, 5): {"color": "darkblue", "pos": (3 / 2 * width, -width)},
            (4, 1): {"color": "darkblue", "pos": (-3 / 4 * width, 3 / 2 * width)},
            (4, 2): {"color": "white", "pos": (0, width)},
            (4, 3): {"color": "white", "pos": (3 / 4 * width, width / 2)},
            (4, 4): {"color": "white", "pos": (3 / 2 * width, 0)},
            (4, 5): {"color": "darkblue", "pos": (9 / 4 * width, -width / 2)},
            (5, 1): {"color": "grey", "pos": (0, 2 * width)},
            (5, 2): {"color": "darkblue", "pos": (3 / 4 * width, 3 / 2 * width)},
            (5, 3): {"color": "darkblue", "pos": (3 / 2 * width, width)},
            (5, 4): {"color": "darkblue", "pos": (9 / 4 * width, width / 2)},
            (5, 5): {"color": "grey", "pos": (3 * width, 0)}
        }

        original_color = piece_color
        if original_color == "black":
            original_color = "darkblue"

        for dx, dy in directions:
            x, y = piece_pos
            while True:
                x += dx
                y += dy
                if x<1 or x>5 or y<1 or y>5 or self.is_tile_occupied((x, y)):
                    break
                if tiles[(x, y)]["color"] != original_color:
                    possible_moves.add((x, y))
                    break
                possible_moves.add((x, y))

        return possible_moves


    def is_valid_move(self, original_position, expected_position):
        piece_color = None
        for piece in self.pieces:
            if piece[0] == original_position:
                piece_color = piece[1]
                break
        if piece_color is None:
            return False
        possible_moves = self.movable_places(original_position, piece_color)
        return expected_position in possible_moves


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
                if x<1 | x>5 | y<1 | y>5:
                    break
                found_piece = None
                for i, piece in enumerate(self.pieces):
                    if piece[0] == (x, y):
                        found_piece = (i, piece[1])
                        break
                if found_piece is None:
                    break
                if found_piece[1] == opponent:
                    to_flip.append(found_piece[0])
                elif found_piece[1] == self.current_player:
                    for idx in to_flip:
                        self.pieces[idx] = (self.pieces[idx][0], self.current_player)
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
        for piece in self.pieces:
            pos, color = piece
            if pos == (-1, -1):
                continue
            for dx, dy in directions:
                count = 1
                x, y = pos
                while True:
                    x += dx
                    y += dy
                    if not(x<1 or x>5 or y<1 or y>5) and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                x, y = pos
                while True:
                    x -= dx
                    y -= dy
                    if not(x<1 or x>5 or y<1 or y>5) and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                if count >= 5:
                    return color
        return None

    # Check win does not check if the play was a movement, yet to implement
    def check_win(self):
        directions = [
            (0, 1),  # Vertical
            (1, 0),  # Horizontal
            (1, -1)  # Diagonal
        ]
        for piece in self.pieces:
            pos, color = piece
            if pos == (-1, -1):
                continue
            for dx, dy in directions:
                count = 1
                x, y = pos
                while True:
                    x += dx
                    y += dy
                    if not(x<1 or x>5 or y<1 or y>5) and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                x, y = pos
                while True:
                    x -= dx
                    y -= dy
                    if not(x<1 or x>5 or y<1 or y>5) and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                if count == 4:
                    return color
        return None

    def evaluate_board(self, last_play_was_movement):
        opponent = "white" if self.current_player == "black" else "black"

        # Immediate losses (5 in a row) override any other score.
        if self.check_lose() == self.current_player:
            return -10000
        elif self.check_lose() == opponent:
            return 10000

        # Only consider wins if the last move was a movement.
        if last_play_was_movement:
            if self.check_win() == self.current_player:
                return 9000  # Win value; slightly less than immediate win to force blocking moves
            elif self.check_win() == opponent:
                return -9000

        score = 0

        # Threat detection: Check if the opponent can win in one move.
        # (You might simulate each valid play for the opponent and check for an immediate win.)
        for move in self.get_valid_plays():
            if move[0] == "move":
                # Simulate opponent's move if current player were opponent.
                temp_state = copy.deepcopy(self)
                temp_state.current_player = opponent
                temp_state = temp_state.make_move(move)
                if temp_state.check_win() == opponent:
                    score -= 5000  # Large penalty if the opponent can force a win
                    break

        # Alignment scoring: encourage your own alignments and penalize opponent's.
        for (pos, color) in self.pieces:
            align = self.count_alignment(pos, color)
            if color == self.current_player:
                score += align * 10
            else:
                # A strong opponent alignment is even more dangerous.
                score -= align * 20

        # Mobility heuristic: more valid moves is generally better.
        player_moves = len(self.get_valid_plays())
        temp = self.current_player
        self.current_player = opponent
        opp_moves = len(self.get_valid_plays())
        self.current_player = temp
        score += (player_moves - opp_moves) * 5

        return score


    def count_alignment(self, position, player):

        # Returns a score based on how many pieces are aligned

        directions = [(0, 1), (1, 0), (1, -1)]
        total_score = 0

        for dx, dy in directions:
            count = 1
            x, y = position

            # Forward search
            while not(x-dx<1 or x-dx>5 or y-dy<1 or y-dy>5) and any(p[0] == (x + dx, y + dy) and p[1] == player for p in self.pieces):
                count += 1
                x += dx
                y += dy

            # Backward search
            x, y = position
            while not(x-dx<1 or x-dx>5 or y-dy<1 or y-dy>5) and any(p[0] == (x - dx, y - dy) and p[1] == player for p in self.pieces):
                count += 1
                x -= dx
                y -= dy

            if count == 3:
                total_score += 5
            elif count == 2:
                total_score += 2

        return total_score

