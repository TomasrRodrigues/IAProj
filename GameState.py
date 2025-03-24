
import GameConstants
import copy


width=GameConstants.width

class GameState:
    def __init__(self):
        self.tiles =  {
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
        self.reset()

    #Function to reset the board state (no pieces)
    def reset(self):
        self.pieces = []

        self.reserve = {"black": 6, "white": 6}

        self.current_player = "black"
        self.dragging_piece = None
        self.dragging_pos = None


    #Function to place a piece
    def place_piece(self, tile, color):
        if(self.is_tile_occupied(tile)):
            print ("Tile already occupied")
            return None
        if self.reserve[color]<=0:
            print(f"No {color} pieces left to place")
            return None
        self.pieces.append((tile, color))
        self.reserve[color]-=1


    #Function to make a move (should be checked if it's valid before, not cheking here)
    #Returns new state of the board
    def make_move(self, move):
        new_state = copy.deepcopy(self)
        piece_pos, new_tile = move  # piece_pos is (x, y) instead of an index

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

    #Get valid plays for a player with a certain state of the board
    def get_valid_plays(self):
        valid_moves = []

        #Get Valid moves
        for index, (piece_pos, piece_color) in enumerate(self.pieces):
            if piece_color!=self.current_player:
                continue
            moves= self.movable_places(piece_pos, piece_color)
            for move in moves:
                valid_moves.append(("move", index, move))

        #Get Valid places
        if self.reserve[self.current_player]>0:
            for tile in self.tiles:
                if not self.is_tile_occupied(tile):
                    valid_moves.append(("place", tile))

        return valid_moves

    #BOOLEAN: Check if a tile is occupied
    def is_tile_occupied(self, tile):
        for piece in self.pieces:
            if piece[0] == tile:
                return True
        return False

    #returns a set of the movable places for a piece
    def movable_places(self, piece_pos, piece_color):
        possible_moves=set()

        directions = [
            (0, 1), (0, -1),  # Vertical
            (1, 0), (-1, 0),  # Horizontal
            (1, -1), (-1, 1)  # Diagonal
        ]

        original_color = piece_color
        if original_color == "black":
            original_color = "darkblue"

        for dx, dy in directions:
            x, y = piece_pos
            while True:
                x += dx
                y += dy
                if (x, y) not in self.tiles or self.is_tile_occupied((x, y)):
                    break
                if self.tiles[(x, y)]["color"] != original_color:
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


    #Function to flip pieces. Does not check if the play was a movement. So it should be checked
    #in the caller
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
                if (x, y) not in self.tiles:
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


    #Check lose function
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
                    if (x, y) in self.tiles and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                x, y = pos
                while True:
                    x -= dx
                    y -= dy
                    if (x, y) in self.tiles and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                if count >= 5:
                    return color
        return None

    #Check win does not check if the play was a movement, yet to implement
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
                    if (x, y) in self.tiles and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                x, y = pos
                while True:
                    x -= dx
                    y -= dy
                    if (x, y) in self.tiles and any(p[0] == (x, y) and p[1] == color for p in self.pieces):
                        count += 1
                    else:
                        break
                if count == 4:
                    return color
        return None


    def evaluate_board(self, last_play_was_movement):

        last_play_was_movement = True

        opponent = "white" if self.current_player == "black" else "black"

        # Check Loss: if 5 in a row appears, it's a loss (even if it was a placement)
        if self.check_lose() == self.current_player:
            return -1000
        if self.check_lose() == opponent:
            return 1000

        score = 0

        # Only reward a win if the last move was a movement
        if last_play_was_movement:
            # For win condition, we call check_win with a valid moved piece's position.
            # (Here, you might need to store or pass in the position of the last moved piece.)
            # For this example, assume we have a variable last_moved_piece_pos.
            #last_moved_piece_pos = original_position  You would implement this
            win_result = self.check_win()
            if win_result == self.current_player:
                return 1000
            elif win_result == opponent:
                return -1000

        # Heuristic: Alignment of pieces (even if from placement moves, they hint at potential)
        for piece in self.pieces:
            pos, color = piece
            if pos == (-1, -1):
                # You might want to add a small bonus for having pieces in reserve
                score += 2 if color == self.current_player else -2
                continue
            # Add alignment score (your count_alignment already gives a value based on 2/3 in a row)
            if color == self.current_player:
                score += self.count_alignment(pos, self.current_player) * 10
            else:
                score -= self.count_alignment(pos, opponent) * 10

        # Heuristic: Mobility (using get_valid_moves which aggregates movable_places)
        player_moves = len(self.get_valid_plays())
        temp = self.current_player
        self.current_player = opponent
        opponent_moves = len(self.get_valid_plays())
        self.current_player = temp
        score += (player_moves - opponent_moves) * 5

        return score

    def count_alignment(self, position, player):

        # Returns a score based on how many pieces are aligned

        directions = [(0, 1), (1, 0), (1, -1)]
        total_score = 0

        for dx, dy in directions:
            count = 1
            x, y = position

            # Forward search
            while (x + dx, y + dy) in self.tiles and any(p[0] == (x + dx, y + dy) and p[1] == player for p in self.pieces):
                count += 1
                x += dx
                y += dy

            # Backward search
            x, y = position
            while (x - dx, y - dy) in self.tiles and any(p[0] == (x - dx, y - dy) and p[1] == player for p in self.pieces):
                count += 1
                x -= dx
                y -= dy

            if count == 3:
                total_score += 5
            elif count == 2:
                total_score += 2

        return total_score

