from datetime import datetime, timedelta
from abc import abstractmethod


class Field:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        self.square = None
        self.maturation_date = None
        self.productivity = None

        self.harvesting_date = None
        self.harvesting_end = None
        pass

    @abstractmethod
    def set_harvesting_date(self, *args, **kwargs):
        pass


class SimpleField(Field):
    def __init__(self, square: int, maturation_date: datetime, productivity: int):
        self.square = square
        self.maturation_date = maturation_date
        self.productivity = productivity

        self.harvesting_date = maturation_date
        self.harvesting_end = None

    def set_harvesting_date(self, harv_date: datetime):
        self.harvesting_date = harv_date


# class FieldPack(Field):
#     def __init__(self, *fields: Field):
#         self.fields = fields
#
#         self.square = sum([field.square for field in self.square])
#
#     def set_harvesting_date(self, *args, **kwargs):
#         pass
