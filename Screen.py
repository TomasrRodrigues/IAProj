import pygame
import sys
from GameState import GameState
from GameConstants import width, center_pos
from GameTreeNode import GameTreeNode, GameTree
from minimax import minimax
from game import movable_places

state= GameState()
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Yonmoque-Hex Game")
font_small = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 48)

def adjust_pos(pos1, pos2):
    """Helper function: returns the sum of two position vectors."""
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

def draw_text(text, pos, font, color="black"):
    """Helper function to draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

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
                    choose_game_screen()  # Choose Game
                elif event.key == pygame.K_2:
                    instructions_screen() # Instructions
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()

def choose_game_screen():
    while True:
        screen.fill("lightgoldenrod")
        draw_text("Choose your game mode", (500, 150), font_large)
        draw_text("1. Person vs Person", (550, 250), font_small)
        draw_text("2. Person vs Computer", (550, 300), font_small)
        draw_text("3. Computer vs Computer", (550, 350), font_small)
        draw_text("4. Go Back", (550, 400), font_small)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop("pvp")
                    return
                elif event.key == pygame.K_2:
                    game_loop("pvc")
                    return
                elif event.key == pygame.K_3:
                    return "cvc"
                elif event.key == pygame.K_4:
                    return "back"

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

def drawBoard():
    for tile in state.tiles:
        cur = state.tiles[tile]
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

def drawWaitingPieces():
    x = 100
    y = 50
    radius = width / 4

    # Draw the circle
    pygame.draw.circle(screen, "black", (x, y), radius)
    pygame.draw.circle(screen, "black", (x, y), radius, 1)

    # Render the text and get its size
    text_surface = font_small.render(str(state.reserve["black"]), True, "white")
    text_rect = text_surface.get_rect(center=(x, y))  # Center the text inside the circle

    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)

    #draw for white
    x = 100
    y = 600
    radius = width / 4

    # Draw the circle
    pygame.draw.circle(screen, "white", (x, y), radius)
    pygame.draw.circle(screen, "white", (x, y), radius, 1)

    # Render the text and get its size
    text_surface = font_small.render(str(state.reserve["white"]), True, "black")
    text_rect = text_surface.get_rect(center=(x, y))  # Center the text inside the circle

    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)

def drawPieces():
    for piece in state.pieces:
        if piece[0] == (-1, -1):
            continue
        tile = state.tiles[piece[0]]
        pos = adjust_pos(tile["pos"], center_pos)
        pygame.draw.circle(screen, piece[1], pos, width / 4)
        pygame.draw.circle(screen, "black", pos, width / 4, 1)

def drawDraggingPiece():
    if state.dragging_piece is not None and state.dragging_pos is not None:
        pygame.draw.circle(screen, state.pieces[state.dragging_piece][1], state.dragging_pos, width / 4)
        pygame.draw.circle(screen, "black", state.dragging_pos, width / 4, 1)

def getComputerMove(depth):
    best_value, best_move = minimax(
        state,
        depth=depth,  # Set appropriate depth for the AI
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing_player=True,  # The computer (AI) plays as "white"
        last_play_was_movement=False
    )
    print("Computer's best move:", best_move)
    return best_move


def game_loop(mode):
    global state
    selected_piece = None # selected piece to move (if is not None, selected_outside must be)
    selected_tile = None # selected tile to place or move
    selected_outside = None #if it is selected outside (to place)
    last_play_was_move = False



    # Build the game tree up to the desired depth.
    #best_value, best_move = minimax(
    #    state,
    #    depth=5,
    #    alpha=float('-inf'),
    #    beta=float('inf'),
    #    maximizing_player=True,  # Corrected here
    #    last_play_was_movement=False  # Or True, depending on the last action
    #)

    #print("Best move:", best_move)
    # Run the minimax algorithm to determine the best move
    if mode == "pvp":
        while True:
            screen.fill("lightgoldenrod")
            drawBoard()
            drawWaitingPieces()
            drawPieces()
            pygame.display.flip()

            #Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # When the mouse button is pressed down
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #state.get_valid_plays()
                    mouse_x, mouse_y = event.pos

                    #Reserve area coordinates
                    reserve_x, reserve_y = 100, 50 if state.current_player == "black" else 600
                    radius = width / 4

                    # Check if the mouse is clicked within the reserve circle
                    if ((mouse_x - reserve_x) ** 2 + (mouse_y - reserve_y) ** 2) ** 0.5 <= radius:
                        # If he has pieces in reserve, mark that a reserve piece is selected
                        if state.reserve[state.current_player] > 0:
                            selected_piece = None
                            selected_tile = None
                            selected_outside = state.current_player

                    else:
                        # If reserve area is not clicked, check if an on-board tile was clicked
                        for tile in state.tiles:
                            center = adjust_pos(state.tiles[tile]["pos"], center_pos)
                            #If the click was within the area of the tile
                            if ((mouse_x - center[0]) ** 2 + (mouse_y - center[1]) ** 2) ** 0.5 <= width / 2:
                                # If not occupied
                                if not state.is_tile_occupied(tile):
                                    #If it was selected outside before place it
                                    if selected_outside is not None:
                                        state = state.place_piece(tile, selected_outside)
                                        state.current_player = "white" if state.current_player == "black" else "black"
                                        selected_piece = None
                                        selected_tile = None
                                        selected_outside = None
                                    elif selected_piece is not None:
                                        mov_places = state.movable_places(selected_piece, state.current_player)
                                        if tile not in mov_places:
                                            print("Not a valid move")
                                            continue
                                        state = state.make_move((selected_piece, tile))
                                        state.current_player = "white" if state.current_player == "black" else "black"
                                        selected_piece=None
                                        selected_tile=None
                                        selected_outside=None
                                        last_play_was_move=True

                                else:
                                    piece_at_the_tile = state.get_piece_at(tile)
                                    if piece_at_the_tile is not None:
                                        if piece_at_the_tile[1]==state.current_player:
                                            selected_piece=piece_at_the_tile[0]
                                            selected_tile=None
                                            selected_outside=None



            loser=state.check_lose()

            if loser is not None:
                print(f"Loser: {loser}")
                return
            if last_play_was_move:
                winner = state.check_win()
                if winner is not None:
                    print(f"Winner: {winner}")
                    return
                last_play_was_move=False

    elif mode == "pvc":
        while True:
            screen.fill("lightgoldenrod")
            drawBoard()
            drawWaitingPieces()
            drawPieces()
            pygame.display.flip()

            # Player's Turn (Black)
            if state.current_player == "black":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos

                        # Reserve area coordinates
                        reserve_x, reserve_y = 100, 50 if state.current_player == "black" else 600
                        radius = width / 4

                        # Check if the mouse is clicked within the reserve circle
                        if ((mouse_x - reserve_x) ** 2 + (mouse_y - reserve_y) ** 2) ** 0.5 <= radius:
                            # If the player has pieces in reserve, select a piece
                            if state.reserve[state.current_player] > 0:
                                selected_piece = None
                                selected_tile = None
                                selected_outside = state.current_player

                        else:
                            # If reserve area is not clicked, check if an on-board tile was clicked
                            for tile in state.tiles:
                                center = adjust_pos(state.tiles[tile]["pos"], center_pos)
                                if ((mouse_x - center[0]) ** 2 + (mouse_y - center[1]) ** 2) ** 0.5 <= width / 2:
                                    if not state.is_tile_occupied(tile):  # If the tile is not occupied
                                        if selected_outside is not None:
                                            state = state.place_piece(tile, selected_outside)
                                            state.current_player = "white"
                                            selected_piece = None
                                            selected_tile = None
                                            selected_outside = None
                                        elif selected_piece is not None:
                                            mov_places = state.movable_places(selected_piece, state.current_player)
                                            if tile not in mov_places:
                                                print("Not a valid move")
                                                continue
                                            state = state.make_move((selected_piece, tile))
                                            state.current_player = "white"
                                            selected_piece = None
                                            selected_tile = None
                                            selected_outside = None
                                            last_play_was_move = True

                # Check for win or loss conditions
                loser = state.check_lose()
                if loser is not None:
                    print(f"Loser: {loser}")
                    return
                if last_play_was_move:
                    winner = state.check_win()
                    if winner is not None:
                        print(f"Winner: {winner}")
                        return
                    last_play_was_move = False

            # Computer's Turn (White)
            elif state.current_player == "white":
                print("Computer's turn!")
                # AI tries to maximize from White's perspective
                best_move = getComputerMove(depth=3)
                if best_move is not None:
                    if best_move[0] == "place":
                        state = state.place_piece(best_move[1], "white")
                        last_play_was_move = False
                    elif best_move[0] == "move":
                        state = state.make_move(best_move)
                        last_play_was_move = True
                # Switch turn back to black
                state.current_player = "black"

                # Check losing
                loser = state.check_lose()
                if loser is not None:
                    print(f"Loser: {loser}")
                    return
                # If last move was a movement, check winning
                if last_play_was_move:
                    winner = state.check_win()
                    if winner is not None:
                        print(f"Winner: {winner}")
                        return
                    last_play_was_move = False

                pygame.time.wait(1000)


if __name__ == '__main__':
    choice = home_screen()
    print("User selected:", choice)
    pygame.quit()