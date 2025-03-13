# Example file showing a circle moving on screen
import pygame

width = 100

tiles = {(1,1):{"color":"grey","pos":(-3*width,0)},              (1,2):{"color":"darkblue","pos":(9/4*width,-width/2)}, (1,3):{"color":"darkblue","pos":(3/2*width,-width)},(1,4):{"color":"darkblue","pos":(3/4*width,-3/2*width)},(1,5):{"color":"grey","pos":(0,-2*width)},
         (2,1):{"color":"darkblue","pos":(-9/4*width,width/2)},  (2,2):{"color":"white","pos":(-3/2*width,0)},          (2,3):{"color":"white","pos":(3/4*width,-width/2)}, (2,4):{"color":"white","pos":(0,-width)},               (2,5):{"color":"darkblue","pos":(-3/4*width,-3/2*width)},
         (3,1):{"color":"darkblue","pos":(-3/2*width,width)},    (3,2):{"color":"white","pos":(-3/4*width,width/2)},    (3,3):{"color":"grey","pos":(0,0)},                 (3,4):{"color":"white","pos":(-3/4*width,-width/2)},    (3,5):{"color":"darkblue","pos":(-3/2*width,-width)},
         (4,1):{"color":"darkblue","pos":(-3/4*width,3/2*width)},(4,2):{"color":"white","pos":(0,width)},               (4,3):{"color":"white","pos":(3/4*width,width/2)},  (4,4):{"color":"white","pos":(3/2*width,0)},            (4,5):{"color":"darkblue","pos":(-9/4*width,-width/2)},
         (5,1):{"color":"grey","pos":(0,2*width)},               (5,2):{"color":"darkblue","pos":(3/4*width,3/2*width)},(5,3):{"color":"darkblue","pos":(3/2*width,width)}, (5,4):{"color":"darkblue","pos":(9/4*width,width/2)},   (5,5):{"color":"grey","pos":(3*width,0)}}


#(coord(x,y), color)
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

def adjust_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

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

def drawPieces(l):
    for piece in l:
        if piece[0] == (-1,-1):
            continue
        tile = tiles[piece[0]]
        pos = adjust_pos(tile["pos"], center_pos)
        pygame.draw.circle(screen, piece[1], pos, width/4)
        pygame.draw.circle(screen, "black", pos, width/4, 1)
    return

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#tiles ((x,y), colour)


center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("lightgoldenrod")
    drawBoard(tiles)
    drawPieces(pieces)
    if pygame.mouse.get_pressed()[0]:
        click = pygame.mouse.get_pos()
        pygame.draw.circle(screen, "black", click, 1/4 * width)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
