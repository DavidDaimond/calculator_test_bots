from abc import abstractmethod


class HarvesterPack:
    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def count_area_cov(self):
        pass


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


class GigaHarvPack(HarvesterPack):
    def __init__(self, *subpacks: list[HarvesterPack]):
        self.subpacks = subpacks

        self.area_cov = None

    def count_area_cov(self, inline=True):
        area_cov = sum([pack.count_area_cov() for pack in self.subpacks])

        if inline:
            self.area_cov = area_cov

        return area_cov
