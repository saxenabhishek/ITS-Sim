import pygame

pygame.init()
default_font = pygame.font.SysFont("CO59", 32)

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

DEBUG = False


class color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 100, 100)
    OFF_WHITE = (240,) * 3
