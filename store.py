import products


class Store:
    """Store class initiation and methods definitions"""

    def __init__(self, product_list):
        """Store instance initialization"""
        self._list_of_products = product_list

    def __contains__(self, product):
        """Magick method that returns bool weather product is in store"""
        return product in self._list_of_products

    def __add__(self, store):
        """Operator overload. Returns a new store as a sum of two stores"""
        return Store(self._list_of_products + store.all_products)

    def add_product(self, product):
        """adds new product to the store"""
        if product in self._list_of_products:
            pass
        self._list_of_products.append(product)

    def remove_product(self, product):
        """Removes a product from the store"""
        self._list_of_products.remove(product)

    @property
    def total_quantity(self):
        """Returns quantity of all products left is store as integer"""
        return sum(product.quantity for product in self._list_of_products)

    @property
    def all_products(self):
        """Returns list of all active products left in store"""
        return [product for product in self._list_of_products if product.is_active]

    def order(self, shopping_list, product_quantity_reduction=True):
        """Reduced product amount left is store, returns total price of the order
        :param shopping_list: list of tuples (product, quantity)
        :param product_quantity_reduction: bool
        :return: float or integer
        """
        total_price = 0
        for product, quantity in shopping_list:
            if product not in self._list_of_products:
                raise ValueError(f'There is no {product} in the store.')
            for current_product in self._list_of_products:
                if current_product == product:
                    if isinstance(current_product, (products.NonStockedProduct, products.LimitedProduct)):
                        total_price += current_product.buy(quantity)
                    else:
                        total_price += current_product.buy(quantity, product_quantity_reduction)
        return total_price
