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

    def __hash__(self):
        """Makes product instances hashable"""
        return hash((self.name, self.price, self.quantity))

    def __lt__(self, product):
        """Implements lower than comparison of product based on their prices"""
        return self._price < product.price

    def __gt__(self, product):
        """Implements greater than comparison of product based on their prices"""
        return self._price > product.price

    def __ge__(self, product):
        """Implements greater or equal than comparison of product based on their prices"""
        return self._price >= product.price

    def __le__(self, product):
        """Implements lower than or equal comparison of product based on their prices"""
        return self._price <= product.price

    def __eq__(self, product):
        """Implements is equal comparison of product based on their prices"""
        return self._price == product.price

    @property
    def quantity(self):
        """Return quantity of a product instance"""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets product quantity"""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity should be a positive integer.')
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    @property
    def price(self):
        """gets the product price"""
        return self._price

    @property
    def is_active(self):
        """Checks if product is active. Returns bool value"""
        return self._active

    def activate(self):
        """Activates the product"""
        self._active = True

    def deactivate(self):
        """Deactivates the product"""
        self._active = False

    def __str__(self, quantity=0):
        """Returns product info as f-string"""
        result = f'{self._name}, Price: ${self._price}, Quantity: {self._quantity - quantity}'
        if self._promotions:
            result += "".join([", " + str(promo_name) for promo_name in self._promotions])
        return result

    def show(self, quantity=0):
        """Returns product info as f-string"""
        result = f'{self._name}, Price: ${self._price}, Quantity: {self._quantity - quantity}'
        if self._promotions:
            result += "".join([", " + str(promo_name) for promo_name in self._promotions])
        return result

    @property
    def name(self):
        """Returns product name"""
        return self._name

    def buy(self, quantity, reduce_product_quantity=True):
        """Implements buy functionality.
        Reduces product amount if provided quantity is valid and reduce_product_quantity is True.
        Applies promotions, returns total price
        :param quantity: amount of a product bought
        :param reduce_product_quantity: bool
        :return: float
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Quantity should be a positive integer.')
        if quantity > self._quantity:
            raise ValueError(f'Quantity can not be bigger than items in store ({self._quantity}).')
        if reduce_product_quantity:
            self.quantity = self._quantity - quantity
        if self._promotions:
            promo_multiplier = 1
            for promo in self._promotions:
                promo_multiplier *= promo.apply_promotion(self, quantity)
            return round(self._price * promo_multiplier * quantity, 2)
        return round(quantity * self._price, 2)

    def set_promotion(self, promotion):
        """Adds a promotion to the product promotions set"""
        self._promotions.add(promotion)

    def remove_promotion(self, promotion):
        """Removes a promotion from the product promotions set"""
        self._promotions.remove(promotion)


class NonStockedProduct(Product):
    """Non stocked product class"""

    def __init__(self, name, price):
        """Instance initiation"""
        super().__init__(name, price, quantity=0)

    def __str__(self, quantity=0):
        """Returns product info as f-string"""
        result = f'{self._name}, Price: ${self._price}'
        if self._promotions:
            result += "".join([", " + str(promo_name) for promo_name in self._promotions])
        return result

    def buy(self, quantity, reduce_product_quantity=False):
        """Implements buy functionality. Applies promotions, returns total price
        :param quantity: amount of a product bought
        :param reduce_product_quantity: bool
        :return: float
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Quantity should be a positive integer.')
        self.quantity = quantity
        if self._promotions:
            promo_multiplier = 1
            for promo in self._promotions:
                promo_multiplier *= promo.apply_promotion(self, quantity)
            return round(self._price * promo_multiplier * quantity, 2)
        return round(quantity * self._price, 2)


class LimitedProduct(Product):
    """Class for Limited products"""

    def __init__(self, name, price, maximum, quantity=0):
        """instance initialization"""
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def __str__(self, quantity=0):
        """Presents instance info as a string"""
        result = f'{self._name}, Price: ${self._price}, Limited to {self._maximum} per order!'
        if self._promotions:
            result += "".join([", " + str(promo_name) for promo_name in self._promotions])
        return result

    def show(self, quantity=0):
        return str(super()).replace(f'Quantity: {self._quantity}',
                                    f'Limited to {self._maximum} per order!')

    @property
    def maximum(self):
        """Returns maximum amount of instance product per order"""
        return self._maximum

    def buy(self, quantity, reduce_product_quantity=False):
        """Implements buy functionality. Applies promotions, returns total price
        :param quantity: amount of a product bought
        :param reduce_product_quantity: bool
        :return: float
        """
        if quantity <= self._maximum:
            if self._promotions:
                promo_multiplier = 1
                for promo in self._promotions:
                    promo_multiplier *= promo.apply_promotion(self, quantity)
                return round(self._price * promo_multiplier * quantity, 2)
            return round(quantity * self._price, 2)
        return f'Error while make order! Only {self._maximum} {self.name()} is allowed!'
