import pygame
from comet import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, Color
from comet.utils import WindowPrinter, stats
from comet.grid_city import GridCity
from datetime import datetime

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

    N0_OF_RUNS = 10

    city = GridCity()

    run_no = 1

    while run:
        clock.tick(FPS)

        t = pygame.time.get_ticks()
        stats.add(t=t / 1000)  # time in seconds

        for event in pygame.event.get():
            run = False if event.type == pygame.QUIT else True
            city.process_event(event)

        if run_no == N0_OF_RUNS:
            run = False
            break

        # WIN.blit(BACKGROUND, (0, 0))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT]:
            filename = str(datetime.now()).replace(" ", "T").replace(":", "-").replace(".", "-")
            pygame.image.save(WIN, f"./in-dev-pics/IMG{filename}.png")

        if (t / 1000) > run_no * 20:
            print("time to reset!")
            run_no += 1
            # city.end_episode_save()
            city.end_run_and_reset()

        WIN.fill(Color.PRUSSIAN_BLUE)

        city.draw_agents(WIN)

        WindowPrinter.write(WIN)

        pygame.display.update()
    pygame.quit()


main()
