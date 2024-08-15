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


bose = Product('Bose QuietComfort Earbuds', 250, 500)
