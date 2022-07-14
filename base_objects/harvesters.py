from abc import abstractmethod
from base_objects.agriculture import *
from base_objects.fields import *

from typing import Union

import numpy as np


class HarvesterPack:
    @abstractmethod
    def __init__(self, *args):
        self.num = None
        self.harv_width = None  # meters
        self.bunker_volume = None  # cube meters
        self.speed = None  # kilometers in hour
        pass

    @abstractmethod
    def count_area_cov(self):
        pass

    @abstractmethod
    def set_workhours(self, workhours: int):
        pass

    @abstractmethod
    def count_fills_per_hour(self, field: Field, agriculture: Agriculture, unloading_time: Union[float, int]):
        pass

    def __str__(self):
        return f'{self.__class__.__name__} num: {self.num} harv_width: {self.harv_width} ' \
               + f'bunker_volume: {self.bunker_volume} speed: {self.speed}'

    def __repr__(self):
        return self.__str__()


class SimpleHarvPack(HarvesterPack):
    def __init__(self, num: int, harv_width: float, bunker_volume: float, speed: int, workhours: int = 12):
        self.num = num
        self.harv_width = harv_width  # meters
        self.bunker_volume = bunker_volume  # cube meters
        self.speed = speed  # kilometers in hour

        self.workhours = workhours

        self.area_cov = None

    def count_area_cov(self, inline=True):
        area_cov = self.num * self.harv_width * self.speed * self.workhours / 10

        if inline:
            self.area_cov = area_cov

        return area_cov

    def set_workhours(self, workhours: int):
        self.workhours = workhours

    def get_workhours(self):
        return self.workhours

    def count_fills_per_hour(self, field: Field, agriculture: Agriculture, unloading_time: Union[float, int]):
        fph = (self.harv_width * self.speed * field.productivity) / (self.bunker_volume * agriculture.volume)
        fph /= 1000
        ttf = fph ** -1
        return ttf


class GigaHarvPack(HarvesterPack):
    def __init__(self, *subpacks: HarvesterPack):
        self.subpacks = subpacks

        self.speed = np.mean([x.speed for x in self.subpacks])
        self.harv_width = np.mean([x.harv_width for x in self.subpacks])
        self.bunker_volume = np.mean([x.bunker_volume for x in self.subpacks])
        self.num = sum([x.num for x in self.subpacks])

        self.area_cov = None

    def count_area_cov(self, inline=True):
        area_cov = sum([pack.count_area_cov() for pack in self.subpacks])

        if inline:
            self.area_cov = area_cov

        return area_cov

    def set_workhours(self, workhours: int):
        for subpack in self.subpacks:
            subpack.set_workhours(workhours)

    def get_workhours(self):
        return self.subpacks[0].get_workhours()

    def count_fills_per_hour(self, field: Field, agriculture: Agriculture, unloading_time: Union[float, int]):
        return np.mean([pack.count_fills_per_hour(field, agriculture, unloading_time) for pack in self.subpacks])

    def __str__(self):
        return self.__class__.__name__ + ' with subpacks:\n' + '\n'.join([x.__str__() for x in self.subpacks])
