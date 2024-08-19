class Product:
    """Defines Product class object and its methods"""

    def __init__(self, name, price, quantity):
        """Initialises an instance of Product class, assigns instance variables
        :param name: string
        :param price: integer or float
        :param quantity: integer
        """
        if not name:
            raise ValueError('Product name can not be empty.')
        self._name = name
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError('Price should be a positive number.')
        self._price = price
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity should be a positive number.')
        self._quantity = quantity
        self._active = True
        self._promotions = set()

    def get_quantity(self):
        """Return quantity of a product instance"""
        return self._quantity

    def set_quantity(self, quantity):
        """Sets product quantity"""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity should be a positive integer.')
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    def get_price(self):
        return self._price

    def is_active(self):
        """Checks if product is active. Returns bool value"""
        return self._active

    def activate(self):
        """Activates the product"""
        self._active = True

    def deactivate(self):
        """Deactivates the product"""
        self._active = False

    def show(self):
        """Returns product info as f-string"""
        result = f'{self._name}, Price: ${self._price}, Quantity: {self._quantity}'
        if self._promotions:
            result += " ".join([", " + str(promo_name) for promo_name in self._promotions])
        return result

    def name(self):
        """Returns product name"""
        return self._name

    def buy(self, quantity):
        """Implements buy functionality.
        Reduces product amount if provided quantity is valid.
        Returns total price
        :param quantity: amount of a product bought
        :return: float or integer
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Quantity should be a positive integer.')
        if quantity > self._quantity:
            raise ValueError(f'Quantity can not be bigger than items in store ({self._quantity}).')
        self.set_quantity(self._quantity - quantity)
        return quantity * self._price

    def set_promotion(self, promotion):
        self._promotions.add(promotion)

    def remove_promotion(self, promotion):
        self._promotions.remove(promotion)


class NonStockedProduct(Product):

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    def show(self):
        return super().show().replace(f'Quantity: {self._quantity}', 'Quantity: Unlimited')

    def buy(self, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Quantity should be a positive integer.')
        return quantity * self._price


class LimitedProduct(Product):

    def __init__(self, name, price, maximum, quantity=0):
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def show(self):
        return super().show().replace(f'Quantity: {self._quantity}',
                                      f'Limited to {self._maximum} per order!')

    def buy(self, quantity):
        if quantity <= self._maximum:
            return quantity * self._price
        return f'Error while make order! Only {self._maximum} {self.name()} is allowed!'
