from abc import ABC, abstractmethod


class Promotion(ABC):
    """abstract class for all promotions"""

    def __init__(self, name):
        """initialise instance"""
        self._name = name

    def __str__(self):
        """magic method for print() and str() functions"""
        return self._name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """abstract method"""
        pass


class SecondHalfPrice(Promotion):
    """promotion class for 'Second half price' promotion"""

    def apply_promotion(self, product, quantity):
        """calculates price multiplier of the promotion depending on quantity of product"""
        if quantity >= 2:
            print(f'\33[34mApplying "{self._name}" promotion for {product.name}\033[00m')
        return ((quantity // 2) * 1.5 + quantity % 2) / quantity


class ThirdOneFree(Promotion):
    """promotion class for 'Third one free' promotion"""

    def apply_promotion(self, product, quantity):
        """calculates price multiplier of the promotion depending on quantity of product"""
        if quantity >= 3:
            print(f'\33[34mApplying "{self._name}" promotion for {product.name}\033[00m')
        return ((quantity // 3) * 2 + quantity % 3) / quantity


class PercentDiscount(Promotion):
    """promotion class for 'Percent discount' promotion"""

    def __init__(self, name, percent):
        """instance initialization"""
        super().__init__(name)
        self._percent = percent

    def apply_promotion(self, product, quantity):
        """calculates price multiplier of the promotion depending on quantity of product and discount percent"""
        print(f'\33[34mApplying "{self._name}" promotion for {product.name}\033[00m')
        return (self._percent * quantity / 100) / quantity
