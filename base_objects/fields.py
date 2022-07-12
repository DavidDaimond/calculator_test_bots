from datetime import datetime, timedelta


class Field:
    def __init__(self, square: int, maturation_date: datetime, productivity: int):
        self.square = square
        self.maturation_date = maturation_date
        self.productivity = productivity

        self.harvesting_date = maturation_date
        self.harvesting_end = None

    def set_harvesting_date(self, harv_date: datetime):
        self.harvesting_date = harv_date
