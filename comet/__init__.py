import pygame

pygame.init()
default_font = pygame.font.Font("comet/asset/SpaceMono-Regular.ttf", 20)

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

SCALE = 0.1  # meters/pixel

DEBUG = 0
FPS = 60


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 100, 100)
    OFF_WHITE = (240,) * 3
    GRAY = (128,) * 3
    STEEL_BLUE = (92, 140, 174, 255)
    TICKLE_ME_PINK = (240, 127, 159, 255)
    AMBER = (255, 191, 0, 255)
    CULTURED = (245, 245, 245, 255)
    PRUSSIAN_BLUE = (5, 44, 74, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
