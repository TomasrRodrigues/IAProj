import pygame
import sys
import time
from GameState import GameState
from GameConstants import width, center_pos
from minimax import minimax
from MonteCarlo import montecarlo


state = GameState()
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Yonmoque-Hex Game")
font_small = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 48)

# Hexagonal board tile configuration (position and color)
# Tile positions and colors defined in a 5x5 grid
    # Format: (x,y): {"color": <color>, "pos": (calculated_position)}
    # ... (tile definitions remain unchanged)
tiles =  {
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


#Helpers for the GUI of the game
def adjust_pos(pos1, pos2):
    """Helper function: returns the sum of two position vectors."""
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])
def draw_text(text, pos, font, color="black"):
    """Helper function to draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


#Screens (missing win screen and choose AI and difficulty)
def home_screen():
    """Display main menu with game options"""
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
    """Display game mode selection screen"""
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
                    game_loop("pvp", None)
                    return
                elif event.key == pygame.K_2:
                    choose_AI_screen()
                    return
                elif event.key == pygame.K_3:
                    game_loop("cvc", None)
                    return
                elif event.key == pygame.K_4:
                    return "back"

def instructions_screen():
    """Display game rules and instructions"""
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

def choose_AI_screen():
    while True:
        screen.fill("lightgoldenrod")
        draw_text("Choose your game mode", (500, 150), font_large)
        draw_text("1. Minimax AI", (550, 250), font_small)
        draw_text("2. MonteCarlo AI", (550, 300), font_small)
        draw_text("4. Go Back", (550, 400), font_small)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choose_ai_difficulty("minimax")
                    return
                elif event.key == pygame.K_2:
                    choose_ai_difficulty("montecarlo")
                    return
                elif event.key == pygame.K_4:
                    return

def choose_ai_difficulty(ai):
    while True:
        screen.fill("lightgoldenrod")
        draw_text("Choose your game mode", (500, 150), font_large)
        draw_text("1. Easy", (550, 250), font_small)
        draw_text("2. Intermediate", (550, 300), font_small)
        draw_text("3. Hard", (550, 350), font_small)
        draw_text("4. Go Back", (550, 500), font_small)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop("pvc", ai, "easy", 50)
                    return
                elif event.key == pygame.K_2:
                    game_loop("pvc", ai, "intermediate", 50)
                    return
                elif event.key == pygame.K_3:
                    game_loop("pvc", ai, "hard", 250)
                    return
                elif event.key == pygame.K_4:
                    return


def win_screen(winner):
    """Display winning screen for 5 seconds."""
    start_time = pygame.time.get_ticks()

    while True:
        # Check if 5 seconds have passed
        if pygame.time.get_ticks() - start_time >= 5000:
            return

        # Handle window closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the screen
        screen.fill("lightgoldenrod")
        if winner is None:
            draw_text("It's a draw!", (500, 300), font_large)
        else:
            draw_text(f"{winner.capitalize()} wins!", (500, 300), font_large)
            draw_text("Returning to main menu in 5 seconds...", (450, 400), font_small)

        pygame.display.flip()
        pygame.time.Clock().tick(30)  # Cap at 30 FPS

def loss_AI_screen():
    start_time = pygame.time.get_ticks()

    while True:
        # Check if 5 seconds have passed
        if pygame.time.get_ticks() - start_time >= 5000:
            return

        # Handle window closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the screen
        screen.fill("lightgoldenrod")


        draw_text(f"You lost!", (500, 300), font_large)
        draw_text(f"My AI was too strong!", (500, 300), font_small)

        draw_text("Returning to main menu in 5 seconds...", (450, 400), font_small)

        pygame.display.flip()
        pygame.time.Clock().tick(30)  # Cap at 30 FPS


def win_AI_screen():
    start_time = pygame.time.get_ticks()

    while True:
        # Check if 5 seconds have passed
        if pygame.time.get_ticks() - start_time >= 5000:
            return

        # Handle window closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the screen
        screen.fill("lightgoldenrod")

        draw_text(f"How is this possible? You defeated my AI", (300, 200), font_large)
        draw_text(f"I will get you next time!", (500, 300), font_small)

        draw_text("Returning to main menu in 5 seconds...", (450, 400), font_small)

        pygame.display.flip()
        pygame.time.Clock().tick(30)  # Cap at 30 FPS


#Drawers for the game
def drawBoard(player):
    """Render the hexagonal game board and current player indicator"""
    if player=="black":
        draw_text("Black Player Turn", (500,50), font_large, color=player)
    else:
        draw_text("White Player Turn", (500, 50), font_large, color=player)
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

def drawHelpButtons():
    minimax_button_rect = pygame.Rect(1000, 300, 250, 50)  # x, y, width, height
    montecarlo_button_rect = pygame.Rect(1000, 400, 250, 50)

    # Draw Minimax Button
    pygame.draw.rect(screen, "white", minimax_button_rect, border_radius=8)
    pygame.draw.rect(screen, "black", minimax_button_rect, 2, border_radius=8)
    text_surface = font_small.render("Help from Minimax", True, "black")
    text_rect = text_surface.get_rect(center=minimax_button_rect.center)
    screen.blit(text_surface, text_rect)

    # Draw MonteCarlo Button
    pygame.draw.rect(screen, "white", montecarlo_button_rect, border_radius=8)
    pygame.draw.rect(screen, "black", montecarlo_button_rect, 2, border_radius=8)
    text_surface = font_small.render("Help from MonteCarlo", True, "black")
    text_rect = text_surface.get_rect(center=montecarlo_button_rect.center)
    screen.blit(text_surface, text_rect)

    return minimax_button_rect, montecarlo_button_rect  # Return rects for click detection

def drawPieces():
    """Render all game pieces on the board"""
    for piece in state.pieces:
        #if piece[0] == (-1, -1):
        #    continue
        tile = tiles[piece[0]]
        pos = adjust_pos(tile["pos"], center_pos)
        pygame.draw.circle(screen, piece[1], pos, width / 4)
        pygame.draw.circle(screen, "black", pos, width / 4, 1)

def getComputerMoveMinimax(depth, ai_color="white"):
    """Get AI move using Minimax algorithm"""
    best_value, best_move = minimax(
        state,
        depth=depth,  # Set appropriate depth for the AI
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing_player=True,  # The computer (AI) plays as "white"
        last_play=None,
        ai_color=ai_color
    )
    print("Computer's best move:", best_move)
    return best_move


def getComputerMoveMonteCarlo(state, depth, ai_color, num_simulations=250):
    best_move = montecarlo(
        state=state,
        rollout_depth=depth,
        num_simulations=num_simulations,
        ai_color=ai_color,
    )
    print("Monte Carlo best move:", best_move)
    return best_move

def game_loop(mode, AIMode, difficulty=None, num_simulations=None):
    """Main game loop handling different play modes
        Args:
            mode: pvp (Player vs Player), pvc (Player vs Computer), cvc (Computer vs Computer)
            AIMode: 'minimax' or 'montecarlo'
            difficulty: AI difficulty level
            num_simulations: Number of MCTS simulations
        """
    global state
    state.reset()
    selected_piece = None  # selected piece to move (if is not None, selected_outside must be)
    selected_tile = None  # selected tile to place or move
    selected_outside = None  # if it is selected outside (to place)
    last_play_was_move = False
    ai_times=[]

    if mode =="pvp":
        while True:
            screen.fill("lightgoldenrod")
            drawBoard(state.current_player)
            drawWaitingPieces()
            minimax_rect, montecarlo_rect = drawHelpButtons()
            drawPieces()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    reserve_x, reserve_y = 100, 50 if state.current_player == "black" else 600
                    radius = width / 4


                    if ((mouse_x - reserve_x) ** 2 + (mouse_y - reserve_y) ** 2) ** 0.5 <= radius:
                        # If he has pieces in reserve, mark that a reserve piece is selected
                        if state.reserve[state.current_player] > 0:
                            selected_piece = None
                            selected_tile = None
                            selected_outside = state.current_player

                    if minimax_rect.collidepoint((mouse_x, mouse_y)):
                        best_move = getComputerMoveMinimax(depth=4, ai_color=state.current_player)
                        if best_move[0]=="move":
                            state = state.make_move(best_move)
                        else:
                            state = state.place_piece(best_move[1], state.current_player)
                        selected_piece = None
                        selected_tile = None
                        selected_outside = None
                        state.current_player = "white" if state.current_player == "black" else "black"

                    elif montecarlo_rect.collidepoint((mouse_x, mouse_y)):
                        best_move = getComputerMoveMonteCarlo(state, depth= 7, ai_color=state.current_player)
                        if best_move[0]=="move":
                            state = state.make_move(best_move)
                        else:
                            state = state.place_piece(best_move[1], state.current_player)
                        selected_piece = None
                        selected_tile = None
                        selected_outside = None
                        state.current_player = "white" if state.current_player == "black" else "black"



                    else:
                        # If reserve area is not clicked, check if an on-board tile was clicked
                        for tile in tiles:
                            center = adjust_pos(tiles[tile]["pos"], center_pos)
                            # If the click was within the area of the tile
                            if ((mouse_x - center[0]) ** 2 + (mouse_y - center[1]) ** 2) ** 0.5 <= width / 2:
                                # If not occupied
                                if not state.is_tile_occupied(tile):
                                    # If it was selected outside before place it
                                    if selected_outside is not None:
                                        state = state.place_piece(tile, selected_outside)
                                        play = ("place", tile)  # Corrected play type

                                        # Check for loss only
                                        print(state.is_game_over(play))
                                        if state.is_game_over(play):
                                            loser = state.check_lose()
                                            winner = "black" if loser == "white" else "white"
                                            win_screen(winner)
                                            return
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
                                        play = ("move", selected_piece, tile)  # Corrected play type

                                        # Check for win/loss
                                        print(state.is_game_over(play))
                                        if state.is_game_over(play):
                                            loser = state.check_lose()
                                            if loser:  # Loss has priority
                                                winner = "black" if loser == "white" else "white"
                                            else:
                                                winner = state.check_win(play)
                                            win_screen(winner)
                                            return
                                        state.current_player = "white" if state.current_player == "black" else "black"
                                        selected_piece = None
                                        selected_tile = None
                                        selected_outside = None
                                        last_play_was_move = True

                                else:
                                    piece_at_the_tile = state.get_piece_at(tile)
                                    if piece_at_the_tile is not None:
                                        if piece_at_the_tile[1] == state.current_player:
                                            selected_piece = piece_at_the_tile[0]
                                            selected_tile = None
                                            selected_outside = None


    if mode == "pvc":
        if AIMode=="minimax":
            if difficulty == "easy":
                depth = 2
            elif difficulty == "intermediate":
                depth = 3
            else:
                depth = 4
            while True:

                screen.fill("lightgoldenrod")
                drawBoard(state.current_player)
                drawWaitingPieces()
                minimax_rect, montecarlo_rect = drawHelpButtons()
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

                            if minimax_rect.collidepoint((mouse_x, mouse_y)):
                                best_move = getComputerMoveMinimax(depth=4, ai_color=state.current_player)
                                if best_move[0] == "move":
                                    state = state.make_move(best_move)
                                else:
                                    state = state.place_piece(best_move[1], state.current_player)
                                selected_piece = None
                                selected_tile = None
                                selected_outside = None
                                state.current_player = "white" if state.current_player == "black" else "black"

                            elif montecarlo_rect.collidepoint((mouse_x, mouse_y)):
                                best_move = getComputerMoveMonteCarlo(state, depth=7, ai_color=state.current_player)
                                if best_move[0] == "move":
                                    state = state.make_move(best_move)
                                else:
                                    state = state.place_piece(best_move[1], state.current_player)
                                selected_piece = None
                                selected_tile = None
                                selected_outside = None
                                state.current_player = "white" if state.current_player == "black" else "black"

                            else:
                                # If reserve area is not clicked, check if an on-board tile was clicked
                                for tile in tiles:
                                    center = adjust_pos(tiles[tile]["pos"], center_pos)
                                    if ((mouse_x - center[0]) ** 2 + (mouse_y - center[1]) ** 2) ** 0.5 <= width / 2:
                                        if not state.is_tile_occupied(tile):  # If the tile is not occupied
                                            if selected_outside is not None:
                                                state = state.place_piece(tile, selected_outside)
                                                play = ("place", tile)
                                                state.current_player = "white"
                                                selected_piece = None
                                                selected_tile = None
                                                selected_outside = None
                                            elif selected_piece is not None:
                                                mov_places = state.movable_places(selected_piece, state.current_player)
                                                if tile not in mov_places:
                                                    print("Not a valid move")
                                                    continue
                                                play = ("move", selected_piece, tile)
                                                state = state.make_move((selected_piece, tile))
                                                state.current_player = "white"
                                                selected_piece = None
                                                selected_tile = None
                                                selected_outside = None
                                                last_play_was_move = True

                                            # Check for win or loss conditions
                                            if state.is_game_over(play):
                                                loser = state.check_lose()
                                                print(
                                                    f"Minimax with difficulty {difficulty} Average move time: {sum(ai_times) / len(ai_times)}")
                                                print(f"AiMoves: {len(ai_times)}")
                                                if loser:
                                                    winner = "white" if loser == "black" else "black"
                                                    win_screen(winner)
                                                    return
                                                else:
                                                    winner = state.check_win(play)
                                                    if winner:
                                                        win_screen(winner)
                                                        return

                                        else:
                                            piece_at_the_tile = state.get_piece_at(tile)
                                            if piece_at_the_tile is not None:
                                                if piece_at_the_tile[1] == state.current_player:
                                                    selected_piece = piece_at_the_tile[0]
                                                    selected_tile = None
                                                    selected_outside = None


                elif state.current_player == "white":
                    print("I can get here")
                    start_time = time.time()
                    best_move = getComputerMoveMinimax(depth=depth)
                    move_time=time.time()-start_time
                    ai_times.append(move_time)
                    print(f"Minimax with difficulty {difficulty}: {move_time}")
                    if best_move is not None:
                        if best_move[0] == "place":
                            state = state.place_piece(best_move[1], "white")
                            last_play_was_move = False
                        else:
                            state = state.make_move(best_move)
                            last_play_was_move=True
                    state.current_player = "black"

                    play=best_move
                    if state.is_game_over(play):
                        loser = state.check_lose()
                        print(f"Minimax with difficulty {difficulty} Average move time: {sum(ai_times) / len(ai_times)}")
                        print(f"AiMoves: {len(ai_times)}")
                        if loser:
                            winner = "black" if loser == "white" else "white"
                            win_screen(winner)
                            #print(f"Average time: {sum(ai_times) / len(ai_times)}")
                            return
                        else:
                            winner = state.check_win(play)
                            if winner:
                                win_screen(winner)
                                #print(f"Average time: {sum(ai_times) / len(ai_times)}")
                                return

        if AIMode=="montecarlo":
            if difficulty == "easy":
                depth = 3
            elif difficulty == "intermediate":
                depth = 5
            else:
                depth = 8
            while True:
                screen.fill("lightgoldenrod")
                drawBoard(state.current_player)
                drawWaitingPieces()
                minimax_rect, montecarlo_rect = drawHelpButtons()
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

                            if minimax_rect.collidepoint((mouse_x, mouse_y)):
                                best_move = getComputerMoveMinimax(depth=4, ai_color=state.current_player)
                                if best_move[0] == "move":
                                    state = state.make_move(best_move)
                                else:
                                    state = state.place_piece(best_move[1], state.current_player)
                                selected_piece = None
                                selected_tile = None
                                selected_outside = None
                                state.current_player = "white" if state.current_player == "black" else "black"

                            elif montecarlo_rect.collidepoint((mouse_x, mouse_y)):
                                best_move = getComputerMoveMonteCarlo(state, depth=7, ai_color=state.current_player)
                                if best_move[0] == "move":
                                    state = state.make_move(best_move)
                                else:
                                    state = state.place_piece(best_move[1], state.current_player)
                                selected_piece = None
                                selected_tile = None
                                selected_outside = None
                                state.current_player = "white" if state.current_player == "black" else "black"

                            else:
                                # If reserve area is not clicked, check if an on-board tile was clicked
                                for tile in tiles:
                                    center = adjust_pos(tiles[tile]["pos"], center_pos)
                                    if ((mouse_x - center[0]) ** 2 + (mouse_y - center[1]) ** 2) ** 0.5 <= width / 2:
                                        if not state.is_tile_occupied(tile):  # If the tile is not occupied
                                            if selected_outside is not None:
                                                play = ("place", tile)
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
                                                play = ("move", selected_piece, tile)
                                                state = state.make_move((selected_piece, tile))
                                                state.current_player = "white"
                                                selected_piece = None
                                                selected_tile = None
                                                selected_outside = None
                                                last_play_was_move = True

                                            if state.is_game_over(play):
                                                loser = state.check_lose()
                                                print(
                                                    f"Montecarlo with difficulty {difficulty} Average move time: {sum(ai_times) / len(ai_times)}")
                                                print(f"AiMoves: {len(ai_times)}")
                                                if loser:
                                                    winner = "white" if loser == "black" else "black"
                                                    win_screen(winner)
                                                    return
                                                else:
                                                    winner = state.check_win(play)
                                                    if winner:
                                                        win_screen(winner)
                                                        return
                                        else:
                                            piece_at_the_tile = state.get_piece_at(tile)
                                            if piece_at_the_tile is not None:
                                                if piece_at_the_tile[1] == state.current_player:
                                                    selected_piece = piece_at_the_tile[0]
                                                    selected_tile = None
                                                    selected_outside = None

                    # Check for win or loss conditions
                    loser = state.check_lose()
                    if loser is not None:
                        if loser == "black":
                            loss_AI_screen()
                        print(f"Loser: {loser}")
                        return
                    if last_play_was_move:
                        winner = state.check_win()
                        if winner is not None:
                            if winner == "white":
                                loss_AI_screen()
                            else:
                                win_AI_screen()
                            print(f"Winner: {winner}")
                            return
                        last_play_was_move = False

                elif state.current_player == "white":
                    print("I can get here")
                    start_time = time.time()
                    best_move = getComputerMoveMonteCarlo(state, depth= depth, ai_color="white", num_simulations=num_simulations)
                    move_time = time.time() - start_time
                    ai_times.append(move_time)
                    print(f"Montecarlo with difficulty {difficulty}: {move_time}")
                    if best_move is not None:
                        if best_move[0] == "place":
                            state = state.place_piece(best_move[1], "white")
                            last_play_was_move = False
                        else:
                            state = state.make_move(best_move)
                            last_play_was_move=True


                    play=best_move
                    if state.is_game_over(play):
                        loser = state.check_lose()
                        print(
                            f"Montecarlo with difficulty {difficulty} Average move time: {sum(ai_times) / len(ai_times)}")
                        print(f"AiMoves: {len(ai_times)}")
                        if loser:
                            winner = "black" if loser == "white" else "white"
                            win_screen(winner)
                            return
                        else:
                            winner = state.check_win(play)
                            if winner:
                                win_screen(winner)
                                return
                    state.current_player = "black"
                    pygame.time.wait(500)

    if mode == "cvc":
        while True:
            screen.fill("lightgoldenrod")
            drawBoard(state.current_player)
            drawWaitingPieces()
            drawPieces()
            pygame.display.flip()

            if state.current_player == "black":
                print("I can get here")

                best_move = getComputerMoveMinimax(depth=4, ai_color="black")

                if best_move is not None:
                    if best_move[0] == "place":
                        state = state.place_piece(best_move[1], "black")
                        last_play_was_move = False
                    else:
                        state = state.make_move(best_move)
                        last_play_was_move = True
                state.current_player = "white"

                play = best_move
                if state.is_game_over(play):
                    loser = state.check_lose()
                    if loser:
                        winner = "black" if loser == "white" else "white"
                        win_screen(winner)
                        return
                    else:
                        winner = state.check_win(play)
                        if winner:
                            win_screen(winner)
                            return


            elif state.current_player == "white":
                print("I can get here")

                best_move = getComputerMoveMonteCarlo(state, depth=7, ai_color="white")

                if best_move is not None:
                    if best_move[0] == "place":
                        state = state.place_piece(best_move[1], "white")
                        last_play_was_move = False
                    else:
                        state = state.make_move(best_move)
                        last_play_was_move = True

                play = best_move
                if state.is_game_over(play):
                    loser = state.check_lose()
                    if loser:
                        winner = "black" if loser == "white" else "white"
                        win_screen(winner)
                        return
                    else:
                        winner = state.check_win(play)
                        if winner:
                            win_screen(winner)
                            return
                state.current_player = "black"

            pygame.time.wait(500)


    print(f"Average time: {sum(ai_times)/len(ai_times)}")


if __name__ == '__main__':
    choice=home_screen()
    pygame.quit()