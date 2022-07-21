from abc import abstractmethod


class BaseSleeve:
    @abstractmethod
    def __init__(self, **params):
        pass

    @abstractmethod
    def get_subsleeve(self, weight):
        pass


class WheatSleeve(BaseSleeve):
    def __init__(self, weight: float, humidity: float,
                 gluten: float, protein: float,
                 gdm: int = None, drop_freq: int = None,
                 productivity: int = 750, name: str = None, **params):

        self.weight = weight
        self.humidity = humidity
        self.gluten = gluten
        self.protein = protein

        self.gdm = gdm
        self.drop_freq = drop_freq

        assert not (self.gdm is None) or not (self.drop_freq is None)
        self.productivity = productivity

        self.name = name
        if self.name is None:
            self.name = 'Sleeve of wheat'

    def __str__(self):
        return f'WheatSleeve {self.name}'

    def get_subsleeve(self, weight):
        return WheatSleeve(weight, self.humidity,
                           self.gluten, self.protein,
                           self.gdm, self.drop_freq,)


