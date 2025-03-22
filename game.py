import pygame
import re
import copy

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state  # The game state at this node
        self.parent = parent  # The parent node
        self.children = []  # List of child nodes

    def add_child(self, child_state):
        """Creates a new child node and adds it to the current node."""
        child_node = TreeNode(child_state, parent=self)
        self.children.append(child_node)
        return child_node


# -----------------------------
# Initialization and Setup
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font_small = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 48)
clock = pygame.time.Clock()
dt = 0

# Global game variables
width = screen.get_height() / 8
center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

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

def init_game():
    """Initialize or reset game state."""
    global pieces, current_player, dragging_piece, dragging_pos
    pieces = [
        ((-1, -1), "black"), ((-1, -1), "black"), ((-1, -1), "black"),
        ((-1, -1), "black"), ((-1, -1), "black"), ((-1, -1), "black"),
        ((-1, -1), "white"), ((-1, -1), "white"), ((-1, -1), "white"),
        ((-1, -1), "white"), ((-1, -1), "white"), ((-1, -1), "white")
    ]
    current_player = "black"
    dragging_piece = None
    dragging_pos = None

# -----------------------------
# Utility Functions
# -----------------------------
def adjust_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

def draw_text(text, pos, font, color="black"):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# -----------------------------
# Home Screen and Instructions
# -----------------------------
def home_screen():
    while True:
        screen.fill("lightgoldenrod")
        draw_text("Yonmoque-Hex Game", (500, 150), font_large)
        draw_text("1. Start Game", (550, 250), font_small)
        draw_text("2. Instructions", (550, 300), font_small)
        draw_text("3. Quit", (550, 350), font_small)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choose_game_screen()  # Start game
                elif event.key == pygame.K_2:
                    instructions_screen()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()

def choose_game_screen():
    while True:
        screen.fill("lightgoldenrod")
        draw_text("Choose yout gamestyle", (500, 150), font_large)
        draw_text("1. Person vs Person", (550, 250), font_small)
        draw_text("2. Person vs Computer", (550, 300), font_small)
        draw_text("3. Computer vs Computer", (550, 350), font_small)
        draw_text("4. Go Back", (550, 400), font_small)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()

                if event.key == pygame.K_4:
                    home_screen()


def instructions_screen():
    while True:
        screen.fill("lightgrey")
        draw_text("Instructions:", (550, 150), font_large)
        draw_text("- Place and move pieces strategically.", (350, 250), font_small)
        draw_text("- Flip opponent pieces by surrounding them.", (350, 300), font_small)
        draw_text("- First to align 4 pieces wins!", (350, 350), font_small)
        draw_text("- Careful! If you align 5 you lose!", (350, 400), font_small)
        draw_text("- Choose to play either against another person or the computer.", (350, 450), font_small)
        draw_text("Press B to go back", (500, 550), font_small)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return  # Go back to home screen

def win_screen(winner_color):
    win_message = f"{winner_color.capitalize()} wins!"
    start_ticks = pygame.time.get_ticks()
    while True:
        if (winner_color=="white"):
            screen.fill("lightgreen")
        else:
            screen.fill("darkblue")
        draw_text(win_message, (550, 350), font_large)
        pygame.display.flip()

        # Break after 5 seconds (5000 milliseconds)
        if pygame.time.get_ticks() - start_ticks > 5000:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def drawBoard():
    for tile in tiles:
        cur = tiles[tile]
        center = adjust_pos(cur["pos"], center_pos)
        pygame.draw.polygon(screen, cur["color"], [
            adjust_pos(center, (-width / 2, 0)),
            adjust_pos(center, (-width / 4, width / 2)),
            adjust_pos(center, (width / 4, width / 2)),
            adjust_pos(center, (width / 2, 0)),
            adjust_pos(center, (width / 4, -width / 2)),
            adjust_pos(center, (-width / 4, -width / 2))
        ])
        pygame.draw.polygon(screen, "black", [
            adjust_pos(center, (-width / 2, 0)),
            adjust_pos(center, (-width / 4, width / 2)),
            adjust_pos(center, (width / 4, width / 2)),
            adjust_pos(center, (width / 2, 0)),
            adjust_pos(center, (width / 4, -width / 2)),
            adjust_pos(center, (-width / 4, -width / 2))
        ], 1)

def drawPieces():
    for piece in pieces:
        if piece[0] == (-1, -1):
            continue
        tile = tiles[piece[0]]
        pos = adjust_pos(tile["pos"], center_pos)
        pygame.draw.circle(screen, piece[1], pos, width / 4)
        pygame.draw.circle(screen, "black", pos, width / 4, 1)

def drawDraggingPiece():
    if dragging_piece is not None and dragging_pos is not None:
        pygame.draw.circle(screen, pieces[dragging_piece][1], dragging_pos, width / 4)
        pygame.draw.circle(screen, "black", dragging_pos, width / 4, 1)

def drawWaitingPieces():
    for i, piece in enumerate(pieces):
        if piece[0] == (-1, -1) and piece[1] == current_player:
            x = 100 + (i % 6) * 50
            y = 50 if piece[1] == "black" else 600
            pygame.draw.circle(screen, piece[1], (x, y), width / 4)
            pygame.draw.circle(screen, "black", (x, y), width / 4, 1)

def is_tile_occupied(tile):
    for piece in pieces:
        if piece[0] == tile:
            return True
    return False

def movable_places(piece_pos, piece_color):
    if piece_pos == (-1, -1):
        possible_moves = set()
        for tile in tiles:
            if not is_tile_occupied(tile):
                possible_moves.add(tile)
        return possible_moves

    possible_moves = set()
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
            if (x, y) not in tiles or is_tile_occupied((x, y)):
                break
            if tiles[(x, y)]["color"] != original_color:
                possible_moves.add((x, y))
                break
            possible_moves.add((x, y))
    return possible_moves

def is_valid_move(original_position, expected_position):
    piece_color = None
    for piece in pieces:
        if piece[0] == original_position:
            piece_color = piece[1]
            break
    if piece_color is None:
        return False
    possible_moves = movable_places(original_position, piece_color)
    return expected_position in possible_moves

def flip_pieces(moved_to, original_position, player_color):
    directions = [
        (0, 1), (0, -1),  # Vertical
        (1, 0), (-1, 0),  # Horizontal
        (1, -1), (-1, 1)  # Diagonal
    ]
    if original_position == (-1, -1):
        return None
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
            for i, piece in enumerate(pieces):
                if piece[0] == (x, y):
                    found_piece = (i, piece[1])
                    break
            if found_piece is None:
                break
            if found_piece[1] == opponent_color:
                to_flip.append(found_piece[0])
            elif found_piece[1] == player_color:
                for idx in to_flip:
                    pieces[idx] = (pieces[idx][0], player_color)
                break
            else:
                break

def check_lose():
    directions = [
        (0, 1),  # Vertical
        (1, 0),  # Horizontal
        (1, -1)  # Diagonal
    ]
    for piece in pieces:
        pos, color = piece
        if pos == (-1, -1):
            continue
        for dx, dy in directions:
            count = 1
            x, y = pos
            while True:
                x += dx
                y += dy
                if (x, y) in tiles and any(p[0] == (x, y) and p[1] == color for p in pieces):
                    count += 1
                else:
                    break
            x, y = pos
            while True:
                x -= dx
                y -= dy
                if (x, y) in tiles and any(p[0] == (x, y) and p[1] == color for p in pieces):
                    count += 1
                else:
                    break
            if count >= 5:
                return color
    return None

def check_win(original_position):
    if original_position == (-1, -1):
        return None
    directions = [
        (0, 1),  # Vertical
        (1, 0),  # Horizontal
        (1, -1)  # Diagonal
    ]
    for piece in pieces:
        pos, color = piece
        if pos == (-1, -1):
            continue
        for dx, dy in directions:
            count = 1
            x, y = pos
            while True:
                x += dx
                y += dy
                if (x, y) in tiles and any(p[0] == (x, y) and p[1] == color for p in pieces):
                    count += 1
                else:
                    break
            x, y = pos
            while True:
                x -= dx
                y -= dy
                if (x, y) in tiles and any(p[0] == (x, y) and p[1] == color for p in pieces):
                    count += 1
                else:
                    break
            if count == 4:
                return color
    return None


# -----------------------------
# AI, minimax implementation
# -----------------------------


def evaluate_board(board, player, original_position):
    # Function evaluate board will be critical for the minimax implementation.
    # The objective is to be called at each node in order to attribute a value to each node
    #
    # This function evaluates the state of the board from the perspective of 'player'
    # Receives as a parameter:
    #   - board: (board state) as list
    #   - player: "black" or "white"
    #   - original_position: the position of the piece moved before movement
    #
    # Returns numeric score (the higher the better)

    last_move_was_movement = True

    if original_position == (-1, -1):
        last_move_was_movement = False


    opponent = "white" if player == "black" else "black"

    # Check Loss: if 5 in a row appears, it's a loss (even if it was a placement)
    if check_lose() == player:
        return -1000
    if check_lose() == opponent:
        return 1000

    score = 0

    # Only reward a win if the last move was a movement
    if last_move_was_movement:
        # For win condition, we call check_win with a valid moved piece's position.
        # (Here, you might need to store or pass in the position of the last moved piece.)
        # For this example, assume we have a variable last_moved_piece_pos.
        last_moved_piece_pos = original_position  # You would implement this
        win_result = check_win(last_moved_piece_pos)
        if win_result == player:
            return 1000
        elif win_result == opponent:
            return -1000

    # Heuristic: Alignment of pieces (even if from placement moves, they hint at potential)
    for piece in board:
        pos, color = piece
        if pos == (-1, -1):
            # You might want to add a small bonus for having pieces in reserve
            score += 2 if color == player else -2
            continue
        # Add alignment score (your count_alignment already gives a value based on 2/3 in a row)
        if color == player:
            score += count_alignment(pos, player) * 10
        else:
            score -= count_alignment(pos, opponent) * 10

    # Heuristic: Mobility (using get_valid_moves which aggregates movable_places)
    player_moves = len(get_valid_moves(board, player))
    opponent_moves = len(get_valid_moves(board, opponent))
    score += (player_moves - opponent_moves) * 5

    return score


def count_alignment(position, player):

    # Returns a score based on how many pieces are aligned

    directions = [(0, 1), (1, 0), (1, -1)]
    total_score = 0

    for dx, dy in directions:
        count = 1
        x, y = position

        # Forward search
        while (x + dx, y + dy) in tiles and any(p[0] == (x + dx, y + dy) and p[1] == player for p in pieces):
            count += 1
            x += dx
            y += dy

        # Backward search
        x, y = position
        while (x - dx, y - dy) in tiles and any(p[0] == (x - dx, y - dy) and p[1] == player for p in pieces):
            count += 1
            x -= dx
            y -= dy

        if count == 3:
            total_score += 5
        elif count == 2:
            total_score += 2

    return total_score


def get_valid_moves(board, player):
    valid_moves = []
    for index, (piece_pos, piece_color) in enumerate(board):
        if piece_color == player:
            moves = movable_places(piece_pos, piece_color)
            for move in moves:
                valid_moves.append((index, move))
    return valid_moves


# -----------------------------
# Main Game Loop
# -----------------------------
def game_loop():
    global dragging_piece, dragging_pos, current_player, dt
    running = True
    init_game()  # Reset game state before starting the loop

    while running:
        screen.fill("lightgoldenrod")
        drawBoard()
        drawPieces()
        drawWaitingPieces()
        drawDraggingPiece()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, piece in enumerate(pieces):
                    piece_pos, piece_color = piece

                    # Clicking an unplaced piece (waiting on the side)
                    if piece_pos == (-1, -1) and piece_color == current_player:
                        x = 100 + (i % 6) * 50
                        y = 50 if piece_color == "black" else 600
                        if (mx - x) ** 2 + (my - y) ** 2 < (width / 4) ** 2:
                            dragging_piece = i
                            dragging_pos = (mx, my)
                            break

                    # Clicking an already placed piece
                    elif piece_pos in tiles:
                        center = adjust_pos(tiles[piece_pos]["pos"], center_pos)
                        if (mx - center[0]) ** 2 + (my - center[1]) ** 2 < (width / 4) ** 2:
                            if piece_color == current_player:
                                dragging_piece = i
                                dragging_pos = (mx, my)
                            break

            elif event.type == pygame.MOUSEBUTTONUP and dragging_piece is not None:
                mx, my = event.pos
                for tile in tiles:
                    center = adjust_pos(tiles[tile]["pos"], center_pos)
                    if (mx - center[0]) ** 2 + (my - center[1]) ** 2 < (width / 2) ** 2:
                        original_position = pieces[dragging_piece][0]
                        expected_position = tile
                        if is_valid_move(original_position, expected_position) and not is_tile_occupied(tile):
                            pieces[dragging_piece] = (tile, pieces[dragging_piece][1])
                            flip_pieces(tile, original_position, pieces[dragging_piece][1])

                            # Check for win/loss conditions
                            loser = check_lose()
                            if loser is not None:
                                # Determine the winner as the opposite of the loser
                                winner = "white" if loser == "black" else "black"
                                win_screen(winner)
                                return

                            winner = check_win(original_position)
                            if winner is not None:
                                win_screen(winner)
                                return

                            current_player = "white" if current_player == "black" else "black"
                            possible_moves = movable_places(tile, pieces[dragging_piece][1])
                            print(f"Possible moves for piece at {tile}: {possible_moves}")
                            print(evaluate_board(pieces, current_player, original_position))


                        else:
                            print("Invalid Move - Either not a valid move or tile occupied")
                dragging_piece = None
                dragging_pos = None

            elif event.type == pygame.MOUSEMOTION and dragging_piece is not None:
                dragging_pos = event.pos

        pygame.display.flip()
        dt = clock.tick(60) / 1000


# -----------------------------
# Main Entry Point
# -----------------------------
if __name__ == '__main__':
    while True:
        home_screen()
        game_loop()
