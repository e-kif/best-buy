class Product:

    def __init__(self, name, price, quantity):
        if not name:
            raise ValueError('Product name can not be empty.')
        self._name = name
        if not (isinstance(price, int) or isinstance(price, float)) or price < 0:
            raise ValueError('Price should be a positive number.')
        self._price = price
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity should be a positive number.')
        self._quantity = quantity
        self._active = True

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, quantity):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity should be a positive integer.')
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    def is_active(self):
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def show(self):
        return f'{self._name}, Price: {self._price}, Quantity: {self._quantity}'

    def buy(self, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Quantity should be a positive integer.')
        if quantity > self._quantity:
            raise ValueError(f'Quantity can not be bigger than items in store ({self._quantity}).')
        self.set_quantity(self._quantity - quantity)
        return quantity * self._price


def main():
    bose = Product('Bose QuietComfort Earbuds', 250, 500)
    mac = Product('MacBook Air M2', 1450, 100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())

    bose.set_quantity(1000)
    print(bose.show())


if __name__ == "__main__":
    main()
