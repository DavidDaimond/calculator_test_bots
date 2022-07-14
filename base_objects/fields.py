from datetime import datetime, timedelta, date
from abc import abstractmethod
from typing import Union


class Field:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        self.square = None
        self.maturation_date = None
        self.productivity = None

        self.harvesting_date = None
        self.harvesting_end = None

    @abstractmethod
    def set_harvesting_date(self, *args, **kwargs):
        pass

    def __str__(self):
        return f'Field square: {self.square} productivity: {self.productivity}' + \
               f' maturation_date: {self.maturation_date}'

    def __repr__(self):
        return self.__str__()


class SimpleField(Field):
    def __init__(self, square: int, maturation_date: Union[datetime, date], productivity: int):
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
