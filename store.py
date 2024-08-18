import products


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


def main():
    bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = products.Product("MacBook Air M2", price=1450, quantity=100)

    store = Store([bose, mac])

    pixel = products.Product("Google Pixel 7", price=500, quantity=250)
    store.add_product(pixel)

    print('store total items ==', store.get_total_quantity())
    print('store all products ==', store.get_all_products())

    bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = products.Product("MacBook Air M2", price=1450, quantity=100)

    store = Store([bose, mac])
    print(store.get_total_quantity())
    price = store.order([(bose, 5), (mac, 30), (bose, 10)])
    print(f"Order cost: {price} dollars.")
    print(store.get_total_quantity())

    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    ]

    store = Store(product_list)
    store_products = store.get_all_products()
    print(store.get_total_quantity())
    print(store.order([(store_products[0], 1), (store_products[1], 2)]))
    print(store.get_total_quantity())


if __name__ == "__main__":
    main()
