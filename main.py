import products
import store
import promotions


def print_store_menu(functions_dict):
    """Prints user interface menu
    :param functions_dict: dictionary of dispatcher functions
    :return: None
    """
    title = 'Store Menu'
    print(f'\n   {title}')
    print(f'   {"_" * len(title)}')
    for key, value in functions_dict.items():
        print(f'{key}. {value[0]}')


def print_all_products(store_obj, order_dict={}):
    """Prints information about all available product in store_obj.
    Prints reduced amount of products if called during order creation
    :param store_obj: Store class object
    :param order_dict: order dictionary so far
    :return: None
    """
    print("-" * 5)
    store_products = store_obj.all_products
    if store_obj.total_quantity > 0:
        for index in range(len(store_products)):
            if store_products[index] in order_dict:
                if isinstance(store_products[index], (products.LimitedProduct, products.NonStockedProduct)):
                    print(f'{index + 1}. {store_products[index]}')
                else:
                    print(f'{index + 1}. {store_products[index].show(order_dict[store_products[index]])}')
            else:
                print(f'{index + 1}. {str(store_products[index])}')
    else:
        print("\u001b[31mCurrently we don't have any products. Come back later!\u001b[0m")
    print("-" * 5)


def print_total_amount_in_store(store_obj):
    """Prints total amount of all products
    :param store_obj: Store class object
    :return: None
    """
    total_items = store_obj.total_quantity
    if total_items == 1:
        print(f'\033[0;32mTotal of {total_items} item in store\033[00m')
    else:
        print(f'\033[0;32mTotal of {total_items} items in store\033[00m')


def ask_user_function_number(func_dict):
    """Gets a function number key from user for dispatcher function
    :param func_dict: dictionary for dispatcher function
    :return: string
    """
    while True:
        user_input = input('Please choose a number: ').strip()
        if user_input in func_dict.keys():
            return user_input
        print('\u001b[31mError with your choice! Try again!\u001b[0m')


def ask_user_product_index(store_obj, order_dict={}):
    """Shows products info, gets product index from user input
    :param store_obj: class Store object
    :param order_dict: order dictionary so far
    :return: integer
    """
    product_list = store_obj.all_products
    while True:
        print_all_products(store_obj, order_dict)
        print('When you want to finish your order, enter empty text.')
        index = input('Which product # do you want? ').strip()
        if index == "":
            return index
        if index in [str(num) for num in list(range(1, len(product_list) + 1))]:
            return int(index) - 1
        print('\u001b[31mProduct # should be in a range '
              f'from 1 to {len(product_list)}\u001b[0m')


def ask_user_product_quantity(store_obj, product_index, order_dict={}):
    """Checks available quantity of a product in a store,
    gets quantity of a product for an order from user input,
    checks if desired quantity is available,
    return quantity if valid
    :param store_obj: Store class object
    :param product_index: integer, index of a product to be added to order
    :param order_dict: dictionary of the product already added to an order
    :return: integer or empty string
    """
    while True:
        quantity = input('What amount do you want? ').strip()
        if quantity in ["", "0"]:
            return ""
        try:
            quantity = int(quantity)
        except ValueError:
            print('\u001b[31mAmount should be a positive integer\u001b[0m')
        current_product = store_obj.all_products[product_index]
        already_ordered = order_dict.get(current_product, 0)
        in_store_quantity = current_product.quantity - already_ordered
        if isinstance(current_product, (products.NonStockedProduct, products.LimitedProduct)):
            in_store_quantity = quantity
        if (isinstance(current_product, products.LimitedProduct)
                and already_ordered + quantity > current_product.maximum):
            print(f'\u001b[31mMaximum amount of {str(current_product).split(",")[0]} per order '
                  f'is {current_product.maximum}. '
                  f'You already have {order_dict.get(current_product, 0)} in your order.\u001b[0m')
            continue
        if quantity <= in_store_quantity:
            return quantity
        print(f'\u001b[31mOnly {in_store_quantity} '
              f'{store_obj.all_products[product_index].name} left in the store\u001b[0m')


def calculate_order_price_and_order_dict(store_obj, orders, product_quantity_reduction=True):
    """Calculates order total price, creates dictionary of products that already in the order
    :param store_obj: Store class object
    :param orders: tuple of order info (product index, quantity ordered)
    :param product_quantity_reduction: bool. True if function should deduct ordered amount
    from product quantity left in store
    :return: tuple (float, dict)
    """
    order_dict = {}
    all_products = store_obj.all_products
    order_price = 0
    for index, quantity in orders:
        product = all_products[index]
        if product in order_dict:
            order_dict[product] += quantity
        else:
            order_dict[product] = quantity
    for product, quantity in order_dict.items():
        order_price += store_obj.order([(product, quantity)], product_quantity_reduction)
    return round(order_price, 2), order_dict


def make_order(store_obj):
    """Asks user for product index and quantity,
    calculates total order price, removes ordered products from Store object,
    pretty-prints order info, applied promotions and total price of the order
    :param store_obj: Store class object
    :return: None
    """
    all_products = store_obj.all_products
    order = []
    order_dict = {}
    while True:
        index = ask_user_product_index(store_obj, order_dict)
        if index == "":
            break
        quantity = ask_user_product_quantity(store_obj, index, order_dict)
        if quantity == "":
            continue
        print(f'\033[0;32m{quantity} {all_products[index].name} was added to your order\033[00m')
        order.append((index, quantity))
        total_price, order_dict = calculate_order_price_and_order_dict(store_obj, order, False)
        print(f'\033[0;32mOrder total price so far is ${total_price}\033[00m')
    if order:
        ordered_products = "\n".join(f'\t{quantity} items: {product.name}'
                                     for product, quantity in order_dict.items())
        print(f"\033[0;32mOrder made! You've ordered: \n{ordered_products}\n\033[00m")
        total_price = calculate_order_price_and_order_dict(store_obj, order, True)[0]
        print(f"\033[0;32mTotal payment: ${total_price}\033[00m")


def start(store_obj):
    """Defines function dictionary, implement dispatcher function
    :param store_obj: Store class object
    :return: None
    """
    func_dict = {
        "1": ["List all products in store", print_all_products],
        "2": ["Show total amount in store", print_total_amount_in_store],
        "3": ["Make an order", make_order],
        "4": ["Quit"]
    }
    while True:
        print_store_menu(func_dict)
        func_key = ask_user_function_number(func_dict)
        if func_key == "4":
            print('\033[0;32mThanks fo visiting "Best-Buy" store! Bye.\033[00m')
            break
        func_dict[func_key][1](store_obj)


def main():
    """Setups the Store and runs start function
    :return: None
    """
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=100, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[2].set_promotion(third_one_free)
    product_list[2].set_promotion(second_half_price)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)

    # running dispatcher function
    start(best_buy)


if __name__ == "__main__":
    main()
