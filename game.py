# Example file showing a circle moving on screen
import pygame
import re

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(100, 100, 140, 32)
clock = pygame.time.Clock()
running = True
dt = 0
text = ''
current_player = "black"

width = screen.get_height()/8

# dictionary defining the board, where the key is the tuple for its coord, with the color to be drawn and the position on the screen
tiles = {(1,1):{"color":"grey","pos":(-3*width,0)},              (1,2):{"color":"darkblue","pos":(-9/4*width,-width/2)}, (1,3):{"color":"darkblue","pos":(-3/2*width,-width)},(1,4):{"color":"darkblue","pos":(-3/4*width,-3/2*width)},(1,5):{"color":"grey","pos":(0,-2*width)},
         (2,1):{"color":"darkblue","pos":(-9/4*width,width/2)},  (2,2):{"color":"white","pos":(-3/2*width,0)},          (2,3):{"color":"white","pos":(-3/4*width,-width/2)}, (2,4):{"color":"white","pos":(0,-width)},               (2,5):{"color":"darkblue","pos":(3/4*width,-3/2*width)},
         (3,1):{"color":"darkblue","pos":(-3/2*width,width)},    (3,2):{"color":"white","pos":(-3/4*width,width/2)},    (3,3):{"color":"grey","pos":(0,0)},                 (3,4):{"color":"white","pos":(3/4*width,-width/2)},    (3,5):{"color":"darkblue","pos":(3/2*width,-width)},
         (4,1):{"color":"darkblue","pos":(-3/4*width,3/2*width)},(4,2):{"color":"white","pos":(0,width)},               (4,3):{"color":"white","pos":(3/4*width,width/2)},  (4,4):{"color":"white","pos":(3/2*width,0)},            (4,5):{"color":"darkblue","pos":(9/4*width,-width/2)},
         (5,1):{"color":"grey","pos":(0,2*width)},               (5,2):{"color":"darkblue","pos":(3/4*width,3/2*width)},(5,3):{"color":"darkblue","pos":(3/2*width,width)}, (5,4):{"color":"darkblue","pos":(9/4*width,width/2)},   (5,5):{"color":"grey","pos":(3*width,0)}}

# list of all pieces in the game, 6 black and 6 white at the start
# pieces not placed yet have a coord of (-1,-1)
# (coord(x,y), color)
pieces = [((-1,-1),"black"),
          ((-1,-1),"black"),
          ((-1,-1),"black"),
          ((-1,-1),"black"),
          ((-1,-1),"black"),
          ((-1,-1),"black"),
          ((-1,-1),"white"),
          ((-1,-1),"white"),
          ((-1,-1),"white"),
          ((-1,-1),"white"),
          ((-1,-1),"white"),
          ((-1,-1),"white")]

# vector sum
def adjust_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

# draws the board
def drawBoard(l):
    for tile in l:
        cur = l[tile]
        center = adjust_pos(cur["pos"], center_pos)
        pygame.draw.polygon(screen, cur["color"], [adjust_pos(center, (-width/2, 0)),
                                        adjust_pos(center, (-width/4, width/2)),
                                        adjust_pos(center, (width/4, width/2)),
                                        adjust_pos(center, (width/2, 0)),
                                        adjust_pos(center, (width/4, -width/2)),
                                        adjust_pos(center, (-width/4, -width/2))])
        pygame.draw.polygon(screen, "black", [adjust_pos(center, (-width/2, 0)),
                                        adjust_pos(center, (-width/4, width/2)),
                                        adjust_pos(center, (width/4, width/2)),
                                        adjust_pos(center, (width/2, 0)),
                                        adjust_pos(center, (width/4, -width/2)),
                                        adjust_pos(center, (-width/4, -width/2))], 1)    
    return

# draws all of the pieces from the given list that have been palced on the board
def drawPieces(l):
    for piece in l:
        if piece[0] == (-1,-1):
            continue
        tile = tiles[piece[0]]
        pos = adjust_pos(tile["pos"], center_pos)
        pygame.draw.circle(screen, piece[1], pos, width/4)
        pygame.draw.circle(screen, "black", pos, width/4, 1)
    return

# parses a move input and calls for the move
# returns 0 on success and 1 on failure
def parseInput(text):
    place = re.search("^[(][1-5],[1-5][)]$", text)
    move = re.search("^[(][1-5],[1-5][)][-][(][1-5],[1-5][)]$", text)
    if place: 
        parse = (place.string.strip("()").split(","))
        print((int(parse[0]),int(parse[1])))
        if movePiece((-1,-1), (int(parse[0]),int(parse[1]))): return 1
        return 0
    elif move:
        parse = move.string.split("-")
        ip = parse[0].strip("()").split(",")
        fp = parse[1].strip("()").split(",")
        print((int(ip[0]),int(ip[1])),(int(fp[0]),int(fp[1])))
        if movePiece((int(ip[0]),int(ip[1])),(int(fp[0]),int(fp[1]))): return 1
        return 0
    else:
        print("Invalid input")
        return 1

# calls for move validity check and applies if possible
# returns 0 on success and 1 on failure
def movePiece(ip,fp):
    valid = True

    for piece in pieces:
        if piece[0] == fp: 
            valid = False
            print("Invalid move")
            return 1

    if valid:
        for piece in pieces:
            if piece[0] == ip and piece[1] == current_player:
                n = pieces.index(piece)
                pieces[n] = (fp, piece[1])
                # change to check move validity
                return 0
    print("Invalid move")
    return 1

# checks all valid moves by a given piece
# return a list with said moves
def validMovesPiece(piece):
    # possible directions:
    # change in one of the coordinates (1,1)-
    # inverse change in both coordinates (3,3)-(2,4) or (3,3)-(4,2)
    # if piece not placed, get all free squares
    # if piece is on its own color, can move any number of squares until in another color
    lst = list()
    return lst

# checks all valid moves by a given color
# returns a list with said moves
def validMoves(color):
    lst = []
    for piece in pieces:
        if piece[1] == color: lst.append(validMovesPiece(piece))
    return lst

center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RETURN:
                if not parseInput(text):
                    if current_player == "black": current_player = "white"
                    else: current_player = "black"
                    print(current_player)
                text = ''
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    #print(pieces)
    screen.fill("lightgoldenrod")
    drawBoard(tiles)
    drawPieces(pieces)

    txt_surface = font.render(text, True, "black")
    width_txt = max(200, txt_surface.get_width()+10)
    input_box.w = width_txt
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, "white", input_box, 2)     

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
