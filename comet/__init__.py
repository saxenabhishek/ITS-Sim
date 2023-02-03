import pygame

pygame.init()
default_font = pygame.font.Font("comet/asset/SpaceMono-Regular.ttf", 20)

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

DEBUG = False


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 100, 100)
    OFF_WHITE = (240,) * 3
    STEEL_BLUE = (92, 140, 174, 255)
    TICKLE_ME_PINK = (240, 127, 159, 255)
    AMBER = (255, 191, 0, 255)
    CULTURED = (245, 245, 245, 255)
    PRUSSIAN_BLUE = (5, 44, 74, 255)
