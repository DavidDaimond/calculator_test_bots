from datetime import datetime
from const import CULTURES_VOLUME


class HarvesterPack:
    def __init__(self, num: int, harv_width: float, bunker_volume: float, speed: int):
        self.num = num
        self.harv_width = harv_width  # meters
        self.bunker_volume = bunker_volume  # cube meters
        self.speed = speed  # kilometers in hour
        self.speed = speed  # kilometers in hour

    def two_tier_clean(self, *fields, work_hours: int = 8):
        pass

    def three_tier_clean(self, *fields, work_hours: int = 8):
        pass


class Field:
    def __init__(self, square: int, maturation_date: datetime, productivity: int):
        self.square = square
        self.maturation_date = maturation_date
        self.productivity = productivity
