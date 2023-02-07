import pygame
from comet import SCREEN_HEIGHT, SCREEN_WIDTH, Color, DEBUG, FPS
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
    slow_car = FollowCar(x, y, target)
    slow_car.MAX_ACCELERATION = 0.01

    while run:
        clock.tick(FPS)
        stats.add(t=pygame.time.get_ticks() / 1000)  # time in seconds

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True

        keys_pressed = pygame.key.get_pressed()

        # reset sprites
        if keys_pressed[pygame.K_LSHIFT]:
            car.reset()
            slow_car.reset()

        WIN.blit(BACKGROUND, (0, 0))

        target.draw(WIN)
        car.draw(WIN)
        slow_car.draw(WIN)

        WindowPrinter.write(WIN)

        pygame.display.update()
    pygame.quit()


main()
