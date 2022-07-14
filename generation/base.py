from generation.const import *

from base_objects import *

import random


def random_simple_harv(num_range: tuple = HARV_NUM_RANGE,
                       width_range: tuple = HARV_WIDTH_RANGE,
                       speed_range: tuple = HARV_SPEED_RANGE,
                       bunker_volume_range: tuple = HARV_BUNKER_VOLUME_RANGE,
                       workhours: tuple = WORKHOURS_RANGE
                       ):
    num = random.randint(*num_range)
    harv_width = round(random.random() * width_range[1], 1)
    speed = random.randint(*speed_range)
    bunker_volume = round(random.random() * bunker_volume_range[1], 1)

    workhours = random.randint(*workhours)

    return SimpleHarvPack(num, harv_width, bunker_volume, speed, workhours)


def random_giga_harv(num_subs: int = 3, simple_only: bool = False, recursive: bool = False, simp_params=()):
    if simple_only:
        subpacks = [random_simple_harv(**dict(simp_params)) for i in range(num_subs)]
        return GigaHarvPack(*subpacks)

    subpacks = []

    for i in range(num_subs):
        if random.random() > .5:
            subpacks.append(random_simple_harv(**dict(simp_params)))
        else:
            subpacks.append(random_giga_harv(num_subs=num_subs, simple_only=not recursive, recursive=recursive))

    return GigaHarvPack(*subpacks)


def random_simple_field(square_range: tuple = FIELD_SQUARE_RANGE,
                        prod_range: tuple = FIELD_PROD_RANGE):

    square = random.randint(*square_range)
    productivity = random.randint(*prod_range)
    maturation_date = datetime.today().date()

    return SimpleField(square, maturation_date, productivity)
