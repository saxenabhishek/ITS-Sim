import pygame
from comet import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, Color
from comet.utils import WindowPrinter, stats
from comet.premade_city import PremadePaths
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

    city = PremadePaths.roundabout(city)
    # city = PremadePaths.crossroad(city)

    while run:
        clock.tick(FPS)
        stats.add(t=pygame.time.get_ticks() / 1000)  # time in seconds

        if len(city.trackers) != 0 and len(city.trackers) % 100 == 0:
            city.process_trackers()

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True
            if event.type == city.INSERT_EVENT:
                city.consume_car_event()
            if event.type == city.REDLIGHT_TICK:
                city.consume_redlight_event()

        # keys_pressed = pygame.key.get_pressed()

        # WIN.blit(BACKGROUND, (0, 0))

        WIN.fill(Color.PRUSSIAN_BLUE)

        city.draw_agents(WIN)

        WindowPrinter.write(WIN)

        pygame.display.update()
    pygame.quit()


main()
