import pygame
import re

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
running = True
dt = 0
current_player = "black"
width = screen.get_height() / 8
center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

tiles = {(1, 1): {"color": "grey", "pos": (-3 * width, 0)},
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
         (5, 5): {"color": "grey", "pos": (3 * width, 0)}}

pieces = [((-1, -1), "black"), ((-1, -1), "black"), ((-1, -1), "black"), ((-1, -1), "black"), ((-1, -1), "black"),
          ((-1, -1), "black"),
          ((-1, -1), "white"), ((-1, -1), "white"), ((-1, -1), "white"), ((-1, -1), "white"), ((-1, -1), "white"),
          ((-1, -1), "white")]

dragging_piece = None
dragging_pos = None


def adjust_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


# Function to draw the Board of the game
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
            adjust_pos(center, (-width / 4, -width / 2))])
        pygame.draw.polygon(screen, "black", [
            adjust_pos(center, (-width / 2, 0)),
            adjust_pos(center, (-width / 4, width / 2)),
            adjust_pos(center, (width / 4, width / 2)),
            adjust_pos(center, (width / 2, 0)),
            adjust_pos(center, (width / 4, -width / 2)),
            adjust_pos(center, (-width / 4, -width / 2))], 1)


# Function to draw the placed pieces
def drawPieces():
    for piece in pieces:
        if piece[0] == (-1, -1):
            continue
        tile = tiles[piece[0]]
        pos = adjust_pos(tile["pos"], center_pos)
        pygame.draw.circle(screen, piece[1], pos, width / 4)
        pygame.draw.circle(screen, "black", pos, width / 4, 1)


# Function to draw the piece being dragged
def drawDraggingPiece():
    if dragging_piece is not None and dragging_pos is not None:
        pygame.draw.circle(screen, pieces[dragging_piece][1], dragging_pos, width / 4)
        pygame.draw.circle(screen, "black", dragging_pos, width / 4, 1)


# Function to draw the pieces waiting on the sides (not yet placed)
def drawWaitingPieces():
    for i, piece in enumerate(pieces):
        if piece[0] == (-1, -1) and piece[1] == current_player:
            x = 100 + (i % 6) * 50
            y = 50 if piece[1] == "black" else 600
            pygame.draw.circle(screen, piece[1], (x, y), width / 4)
            pygame.draw.circle(screen, "black", (x, y), width / 4, 1)


# Function to check if a tile is already occupied
def is_tile_occupied(tile):
    for piece in pieces:
        if piece[0] == tile:
            return True
    return False


def movable_places(piece_pos, piece_color):
    if piece_pos == (-1, -1):  # If the piece is not placed
        # Return all unoccupied tile positions
        possible_moves = set()
        for tile in tiles:
            if not is_tile_occupied(tile):  # Check if the tile is unoccupied
                possible_moves.add(tile)
        return possible_moves

    possible_moves = set()
    directions = [
        (0, 1), (0, -1),  # Vertical
        (1, 0), (-1, 0),  # Horizontal
        (1, -1), (-1, 1)  # Diagonal
    ]

    original_color = piece_color  # Get the color of the starting tile

    if original_color == "black":
        original_color = "darkblue"

    for dx, dy in directions:
        x, y = piece_pos
        while True:
            x += dx
            y += dy
            if (x, y) not in tiles or is_tile_occupied((x, y)):  # Stop if out of bounds or occupied
                break
            if tiles[(x, y)]["color"] != original_color:  # Stop if the color changes
                possible_moves.add((x, y))  # Allow one step into the new color
                break
            possible_moves.add((x, y))  # Continue moving on the same color

    return possible_moves


def is_valid_move(original_position, expected_position):
    # Find the piece with the given original_position
    piece_color = None
    for piece in pieces:
        if piece[0] == original_position:
            piece_color = piece[1]
            break

    if piece_color is None:  # If no piece is found at the original position
        return False

    possible_moves = movable_places(original_position, piece_color)
    return expected_position in possible_moves


#Check if (after a move not a place) some pieces are "sandwiched" and flip them
def flip_pieces(moved_to, original_position, player_color):

    directions = [
        (0, 1), (0, -1),  # Vertical
        (1, 0), (-1, 0),  # Horizontal
        (1, -1), (-1, 1)  # Diagonal
    ]

    #Check if it was a movement
    if original_position==(-1, -1):
        return None

    opponent_color = "white" if player_color == "black" else "black"

    for dx, dy in directions:
        x, y = moved_to
        to_flip = []  # Store indices of opponent pieces to flip
        while True:
            x += dx
            y += dy

            if (x, y) not in tiles:  # Out of bounds
                break

            found_piece = None
            for i, piece in enumerate(pieces):
                if piece[0] == (x, y):
                    found_piece = (i, piece[1])
                    break

            if found_piece is None:  # Empty space, no sandwich possible
                break

            if found_piece[1] == opponent_color:
                to_flip.append(found_piece[0])
            elif found_piece[1] == player_color:
                # Flip all opponent pieces in the chain
                for idx in to_flip:
                    pieces[idx] = (pieces[idx][0], player_color)
                break
            else:
                break


def check_lose():

    directions=[
        (0, 1),  # Vertical
        (1, 0),  # Horizontal
        (1, -1)  # Diagonal
    ]

    for piece in pieces:
        pos, color = piece

        if pos==(-1,-1):
            continue
        for dx,dy in directions:
            count=1
            x, y =pos
            while True:
                x+=dx
                y+=dy
                if (x, y) in tiles and any(p[0] == (x,y) and p[1]==color for p in pieces):
                    count+=1
                else:
                    break
            x,y=pos
            while True:
                x-=dx
                y-=dy
                if(x, y) in tiles and any(p[0] == (x,y) and p[1]==color for p in pieces):
                    count+=1
                else:
                    break
            if count>=5:
                return color
    return None

def check_win(original_position):
    if original_position==(-1, -1):
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





# Game Loop
while running:
    screen.fill("lightgoldenrod")
    drawBoard()
    drawPieces()
    drawWaitingPieces()
    drawDraggingPiece()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i, piece in enumerate(pieces):
                piece_pos, piece_color = piece

                # Check if clicking an unplaced piece (waiting on the side)
                if piece_pos == (-1, -1) and piece_color == current_player:
                    x = 100 + (i % 6) * 50
                    y = 50 if piece_color == "black" else 600
                    if (mx - x) ** 2 + (my - y) ** 2 < (width / 4) ** 2:
                        dragging_piece = i
                        dragging_pos = (mx, my)
                        break

                # Check if clicking an already placed piece
                elif piece_pos in tiles:
                    center = adjust_pos(tiles[piece_pos]["pos"], center_pos)
                    if (mx - center[0]) ** 2 + (my - center[1]) ** 2 < (width / 4) ** 2:
                        if piece_color == current_player:  # Ensure only the current player can move
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

                    # Ensure the move is valid and the tile is unoccupied
                    if is_valid_move(original_position, expected_position) and not is_tile_occupied(tile):
                        pieces[dragging_piece] = (tile, pieces[dragging_piece][1])

                        flip_pieces(tile, original_position, pieces[dragging_piece][1])

                        loser=check_lose()
                        if loser is not None:
                            print(f"Player {loser} loses!")
                            running=False

                        winner = check_win(original_position)
                        if winner is not None:
                            print(f"Player {winner} wins!")
                            running=False
                        current_player = "white" if current_player == "black" else "black"

                        possible_moves = movable_places(tile, pieces[dragging_piece][1])


                        print(f"Possible moves for piece at {tile}: {possible_moves}")
                    else:
                        print("Invalid Move - Either not a valid move or tile occupied")

            dragging_piece = None
            dragging_pos = None

        elif event.type == pygame.MOUSEMOTION and dragging_piece is not None:
            dragging_pos = event.pos

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
