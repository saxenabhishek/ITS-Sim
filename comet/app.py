import pygame
from comet import SCREEN_HEIGHT, SCREEN_WIDTH, Color, DEBUG
from comet.agent import FollowCar, Path, straight_road
from comet.utils import WindowPrinter, stats


WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
run = True

BACKGROUND = pygame.image.load("comet/asset/bck.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


def main():
    """
    Main loop
    """
    global run

    # sharp turn path
    origin = (SCREEN_WIDTH / 3, 100)
    path = []
    for i in range(10):
        path.append(straight_road(origin, 5, 10 * i))
        origin = path[-1][-1]
    for i in range(10):
        path.append(straight_road(origin, 5, 10 * -i))
        origin = path[-1][-1]

    target = Path(*path)
    x, y = path[0][0]
    car = FollowCar(x, y, target)
    while run:
        clock.tick(24)

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True

        keys_pressed = pygame.key.get_pressed()

        # reset sprites
        if keys_pressed[pygame.K_LSHIFT]:
            target.reset()
            car.reset()

        WIN.blit(BACKGROUND, (0, 0))

        target.draw(WIN)
        car.draw(WIN)

        if DEBUG:
            pygame.draw.circle(WIN, Color.CULTURED, (target.x, target.y), radius=10)
        WindowPrinter.write(WIN)

        pygame.display.update()
    pygame.quit()


main()
