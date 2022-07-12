from base_objects.harvesters import *
from base_objects.fields import *


class BaseCleaning:
    def __init__(self, harvesters: HarvesterPack, fields: Field, **params):
        """


        :param harvesters:
        :param fields:
        :param params: params of
        possible p
        """
        self.harvesters = harvesters
        self.fields = fields

        for param_name, param in params.items():
            setattr(self, param_name, param)

