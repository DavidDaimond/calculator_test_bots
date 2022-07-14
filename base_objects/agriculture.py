class Agriculture:
    def __init__(self, volume: int, cost_price, grain_price, name='wheat'):
        self.volume = volume

        self.cost_price = cost_price
        self.grain_price = grain_price

        self.name = name

    def __str__(self):
        return f'Agriculture {self.name} with volume: {self.volume}'

    def __repr__(self):
        return self.__str__()
