from comet.city import City
from comet.targets import straight_road, circle_segment_road, Path
from comet import SCREEN_WIDTH, SCREEN_HEIGHT


class PremadePaths:
    @staticmethod
    def crossroad(city: City) -> City:
        city.add_path(
            Path(
                (10, SCREEN_HEIGHT / 2 - 15),
                straight_road(SCREEN_WIDTH, 0),
            ),
            6,
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
                (SCREEN_WIDTH, SCREEN_HEIGHT / 2 + 15),
                straight_road(SCREEN_WIDTH, 180),
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
        return city

    @staticmethod
    def roundabout(city: City) -> City:
        radius = 200
        sepraration = 10
        city.add_path(
            Path(
                (0, SCREEN_HEIGHT / 2 - sepraration),
                straight_road((SCREEN_WIDTH / 2) - radius, 0),
                circle_segment_road(radius, 180 + 10, 180),
                straight_road((SCREEN_WIDTH / 2) - radius, 0),
            ),
            -1,
        )

        city.add_path(
            Path(
                (SCREEN_WIDTH, SCREEN_HEIGHT / 2 + sepraration),
                straight_road((SCREEN_WIDTH / 2) - radius, 180),
                circle_segment_road(radius, 180 + 10),
                straight_road((SCREEN_WIDTH / 2) - radius, 180),
            ),
            -1,
        )

        city.add_path(
            Path(
                (SCREEN_WIDTH / 2 - sepraration, SCREEN_HEIGHT),
                straight_road(SCREEN_HEIGHT / 2 - radius, 360 - 90),
                circle_segment_road(radius, 180 + 10, 90),
                straight_road(SCREEN_HEIGHT / 2 - radius, 360 - 90),
            ),
            -1,
        )

        city.add_path(
            Path(
                (SCREEN_WIDTH / 2 + sepraration, 0),
                straight_road(SCREEN_HEIGHT / 2 - radius, 90),
                circle_segment_road(radius, 180 + 10, 360 - 90),
                straight_road(SCREEN_HEIGHT / 2 - radius, 90),
            ),
            -1,
        )

        return city
