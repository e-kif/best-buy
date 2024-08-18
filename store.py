class Store:

    def __init__(self, product_list):
        self._list_of_products = product_list

    def add_product(self, product):
        if product in self._list_of_products:
            pass
        self._list_of_products.append(product)

    def remove_product(self, product):
        self._list_of_products.remove(product)

    def get_total_quantity(self):
        return sum(product.get_quantity() for product in self._list_of_products)

    def get_all_products(self):
        return [product for product in self._list_of_products if product.is_active()]

    def order(self, shopping_list):
        total_price = 0
        for product, quantity in shopping_list:
            if product not in self._list_of_products:
                raise ValueError(f'There is no {product} in the store.')
            total_price += [pr.buy(quantity) for pr in self._list_of_products if pr == product][0]
        return total_price
