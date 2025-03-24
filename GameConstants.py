import pygame
import re
import copy

pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
font_small = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 48)
clock = pygame.time.Clock()
dt = 0
width = screen.get_height() / 8
center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)