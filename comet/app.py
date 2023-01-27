import pygame

from comet import SCREEN_HEIGHT, SCREEN_WIDTH, color
from comet.agent.car import BasicCar
from comet.utils import console_stats

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
run = True


def main():
    global run
    sprite = BasicCar(100, 100)
    while run:
        clock.tick(24)

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True

        WIN.fill(color.OFF_WHITE)

        keys_pressed = pygame.key.get_pressed()

        # reset sprite
        if keys_pressed[pygame.K_LSHIFT]:
            del sprite
            sprite = BasicCar(100, 100)
        sprite.draw(WIN)
        console_stats.add(mou_x=pygame.mouse.get_pos()[0], mou_y=pygame.mouse.get_pos()[1])

        console_stats.write()

        pygame.display.update()
    pygame.quit()


main()
