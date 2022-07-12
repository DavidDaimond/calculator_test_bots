from base_objects.harvesters import *
from base_objects.fields import *

from typing import Union
from numpy import argmin


class BaseCleaning:
    BASE_HUMIDITY = .145
    DRY_RATE = ((.14, .02), (.11, .009), (.09, .005),
                (.07, .003), (.06, .002), (.0, .001))

    WEATHER_COEFS = (('sun', 1), ('cloudly', .8), ('rainy', .6))

    def __init__(self, harvesters: HarvesterPack, fields: Field,
                 humidity: float = .18, weather_type: Union[str, int, float] = 1, **params):
        """

        :param harvesters: HarvPack for cleaning
        :param fields: Fields to clean
        :param params: params of cleaning
        """
        self.harvesters = harvesters
        self.fields = fields

        self.humidity = humidity
        self.base_humidity = BaseCleaning.BASE_HUMIDITY

        w_type = type(weather_type)

        if w_type is float:
            self.dry_coef = weather_type

        elif w_type is str:
            self.dry_coef = dict(BaseCleaning.WEATHER_COEFS)[weather_type]

        elif w_type is int:
            self.dry_coef = [x[1] for x in BaseCleaning.WEATHER_COEFS][weather_type]

        self.days_shift = self.get_days_shift()

        for param_name, param in params.items():
            setattr(self, param_name, param)

    def get_days_shift(self, dry_rate=DRY_RATE):
        i = 0
        hum = self.humidity

        while hum > self.base_humidity:
            dry_rate_ind = argmin(map(lambda x: hum - x, dry_rate))

            hum -= dry_rate[dry_rate_ind]
            i += 1

        return i

