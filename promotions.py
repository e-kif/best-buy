from abc import ABC, abstractmethod


class Promotion(ABC):

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        pass


class SecondHalfPrice(Promotion):

    def apply_promotion(self, product, quantity):
        return product.get_price() * ((quantity // 2) * 1.5 + quantity % 2)


class ThirdOneFree(Promotion):

    def apply_promotion(self, product, quantity):
        return product.get_price() * ((quantity // 3) * 2 + quantity % 3)


class PercentDiscount(Promotion):

    def __init__(self, name, percent):
        super().__init__(name)
        self._percent = percent

    def apply_promotion(self, product, quantity):
        return product.get_price() * self._percent * quantity / 100
