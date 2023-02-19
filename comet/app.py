import pygame
from comet import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, Color
from comet.targets import Path, straight_road, circle_segment_road
from comet.utils import WindowPrinter, stats
from comet.city import City

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

    city = City()

    city.add_path(
        Path(
            (10, SCREEN_HEIGHT / 2 - 15),
            straight_road(SCREEN_WIDTH, 0),
        ),
        12,
    )

    city.add_path(
        Path(
            (SCREEN_WIDTH, SCREEN_HEIGHT / 2 + 15),
            straight_road(SCREEN_WIDTH, 180),
        ),
        12,
    )

    city.add_path(
        Path(
            (SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT),
            straight_road(SCREEN_HEIGHT, 360 - 90),
        ),
        6,
    )

    city.add_path(
        Path(
            (SCREEN_WIDTH / 2 + 15, 0),
            straight_road(SCREEN_HEIGHT, 90),
        ),
        6,
    )
    while run:
        clock.tick(FPS)
        stats.add(t=pygame.time.get_ticks() / 1000)  # time in seconds

        if len(city.trackers) != 0 and len(city.trackers) % 5 == 0:
            city.process_trackers()

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True
            if event.type == city.INSERT_EVENT:
                city.consume_car_event()
            if event.type == city.REDLIGHT_TICK:
                city.consume_redlight_event()

        keys_pressed = pygame.key.get_pressed()

        # reset sprites
        if keys_pressed[pygame.K_LSHIFT]:
            city.reset()

        # WIN.blit(BACKGROUND, (0, 0))

        WIN.fill(Color.PRUSSIAN_BLUE)

        city.draw_agents(WIN)

        WindowPrinter.write(WIN)

        pygame.display.update()
    pygame.quit()


main()
