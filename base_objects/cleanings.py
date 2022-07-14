from base_objects.harvesters import *
from base_objects.fields import *
from base_objects.agriculture import *

from abc import abstractmethod
from typing import Union

from collections import Iterable

from numpy import argmin


class BaseCleaning:
    BASE_HUMIDITY = .145
    DRY_RATE = ((.14, .02), (.11, .009), (.09, .005),
                (.07, .003), (.06, .002), (.0, .001))

    WEATHER_COEFS = (('sun', 1), ('cloudly', .75), ('rainy', .5))

    def __init__(self, harvesters: HarvesterPack,
                 fields: Union[SimpleField, Iterable[SimpleField]], agriculture: Agriculture,
                 humidity: float = .18, weather_type: Union[str, int, float] = 1, **params):
        """
        :param harvesters: HarvPack for cleaning
        :param fields: Fields to clean
        :param params: params of cleaning
        """

        self.harvesters = harvesters
        if not isinstance(fields, Iterable):
            fields = [fields]
        self.fields = fields
        self.agriculture = agriculture

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
        shift = 0
        hum = self.humidity

        while hum > self.base_humidity:
            dry_rate_ind = argmin(map(lambda x: hum - x, dry_rate))

            hum -= round(dry_rate[dry_rate_ind][1] * self.dry_coef, 3)
            shift += 1

        return shift

    @abstractmethod
    def count_clean_time(self):
        """
        Count time need for full harvesting
        """
        pass

    @abstractmethod
    def count_losses(self):
        """
        Count losses of grain and money using current fields and harvs
        """
        pass

    def __str__(self):
        return 'Clean Object\n' + 'Harvesters: \n' + self.harvesters.__str__() + \
               '\nFields: ' + self.fields.__str__() + \
               '\nAgriculture: ' + self.agriculture.__str__()

    def __repr__(self):
        return self.__str__()


class DoubleNodeCleaning(BaseCleaning):
    UNLOADING_TIME = (('harv_to_field_edge', 4), ('harv_to_bunker', 3), ('full_stop', 2))

    def __init__(self, *base_args, unloading_time: Union[str, int, float], **kwargs):
        super(DoubleNodeCleaning, self).__init__(*base_args, **kwargs)

        u_cost_type = type(unloading_time)

        if u_cost_type is float:
            self.unloading_time = unloading_time

        elif u_cost_type is str:
            self.unloading_time = dict(DoubleNodeCleaning.UNLOADING_TIME)[unloading_time]

        elif u_cost_type is int:
            self.unloading_time = [x[1] for x in DoubleNodeCleaning.UNLOADING_TIME][unloading_time]

        self.unloading_time /= 60

    def count_clean_time(self):
        area_coverage = self.harvesters.count_area_cov()

        start_date = self.fields[0].maturation_date - timedelta(days=self.days_shift)

        total_time = 0
        overclean = 0

        print(area_coverage)
        print(start_date)

        for field in self.fields:
            field.harvesting_date = start_date + timedelta(days=round(total_time))

            fph = self.harvesters.count_fills_per_hour(field, self.agriculture)

            waitloss_coef = fph * self.unloading_time
            # print(waitloss_coef)

            print('Waitloss_coef for', field, 'is', waitloss_coef, end='\n\n')

            field_time = (field.square - overclean) / (area_coverage * (1 - waitloss_coef))
            print('Field_time for', field, field_time, end='\n\n')

            overclean = (1 - (field_time % 1)) * area_coverage

            print('Overclean for', field, area_coverage - overclean, end='\n\n')

            total_time += field_time

        return total_time


class TripleNodeCleaning(BaseCleaning):

    def count_clean_time(self):
        area_coverage = self.harvesters.count_area_cov()

        start_date = self.fields[0].maturation_date - timedelta(days=self.days_shift)

        total_time = 0
        overclean = 0

        for field in self.fields:
            field.harvesting_date = start_date + timedelta(days=round(total_time))
            field_time = (field.square - overclean) / area_coverage

            overclean = (1 - (field_time % 1)) * area_coverage

            total_time += field_time

        return total_time
