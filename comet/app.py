import pygame
import random

from comet import SCREEN_HEIGHT, SCREEN_WIDTH, color
from comet.agent.basic_car import BasicCar
from comet.agent.follow_car import FollowCar
from comet.utils import console_stats

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
run = True

BACKGROUND = pygame.image.load("comet/asset/bck.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

class FollowTarget:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    global run
    target = FollowTarget(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    sprite = FollowCar(100, 100, target)
    user = BasicCar(100, 100)
    while run:
        clock.tick(24)

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True

        keys_pressed = pygame.key.get_pressed()

        # reset sprites
        if keys_pressed[pygame.K_LSHIFT]:
            user = BasicCar(200, 100)
            sprite = FollowCar(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), target)

        WIN.fill(color.OFF_WHITE)

        WIN.blit(BACKGROUND, (0, 0))

        pygame.draw.circle(WIN, color.RED, (target.x, target.y), radius=10)

        console_stats.write()

        pygame.display.update()
    pygame.quit()


main()
