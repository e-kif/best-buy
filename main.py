import products
import store


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


def print_all_products(store_obj):
    """Prints information about all available product in store_obj
    :param store_obj: Store class object
    :return: None
    """
    print("-" * 5)
    store_products = store_obj.get_all_products()
    if store_obj.get_total_quantity() > 0:
        [print(f'{index + 1}. {store_products[index].show()}')
         for index in range(len(store_products))]
    else:
        print("\u001b[31mCurrently we don't have any products. Come back later!\u001b[0m")
    print("-" * 5)


def print_total_amount_in_store(store_obj):
    """Prints total amount of all products
    :param store_obj: Store class object
    :return: None
    """
    total_items = store_obj.get_total_quantity()
    if total_items == 1:
        print(f'\033[0;32mTTotal of {total_items} item in store\033[00m')
    else:
        print(f'\033[0;32mTotal of {total_items} items in store\033[00m')


def ask_user_function_numer(func_dict):
    """Gets a function number key from user for dispatcher function
    :param func_dict: dictionary for dispatcher function
    :return: string
    """
    while True:
        user_input = input('Please choose a number: ').strip()
        if user_input in func_dict.keys():
            return user_input
        print('\u001b[31mError with your choice! Try again!\u001b[0m')


def ask_user_product_index(store_obj):
    """Gets product index from user
    :param store_obj: class Store object
    :return: integer
    """
    product_list = store_obj.get_all_products()
    while True:
        print_all_products(store_obj)
        print('When you want to finish your order, enter empty text.')
        index = input('Which product # do you want? ').strip()
        if index == "":
            return index
        if index in [str(num) for num in list(range(1, len(product_list) + 1))]:
            return int(index) - 1
        print('\u001b[31mProduct # should be in a range '
              f'from 1 to {len(product_list)}\u001b[0m')


def ask_user_product_quantity(store_obj, product_index):
    """Checks available quantity of a product in a store,
    gets quantity of a product for an order, checks if desired quantity is available,
    return quantity if available
    :param store_obj: Store class object
    :param product_index: integer, index of a product to be added to order
    :return: integer or empty string
    """
    in_store_quantity = store_obj.get_all_products()[product_index].get_quantity()
    while True:
        quantity = input('What amount do you want? ').strip()
        if quantity in ["", "0"]:
            return ""
        try:
            quantity = int(quantity)
        except ValueError:
            print('\u001b[31mAmount should be a positive integer\u001b[0m')
        if quantity <= in_store_quantity:
            return quantity
        print(f'\u001b[31mOnly {in_store_quantity} '
              f'{store_obj.get_all_products()[product_index].name()} left in the store\u001b[0m')


def make_order(store_obj):
    """Shows user all available products, asks user for product index and quantity,
    calculates total order price, removes ordered products from Store object,
    pretty-prints order info and total price of the order
    :param store_obj: Store class object
    :return: None
    """
    all_products = store_obj.get_all_products()
    total_price = 0
    order = []
    while True:
        index = ask_user_product_index(store_obj)
        if index == "":
            break
        quantity = ask_user_product_quantity(store_obj, index)
        if quantity == "":
            continue
        total_price += store_obj.order([(all_products[index], quantity)])
        order.append((index, quantity))
        print(f'\033[0;32m{quantity} {all_products[index].name()} was added to your order')
        print(f'Order total price so far is ${total_price}\033[00m')
    # converting order list into user-friendly list of ordered items
    order_dict = {}
    for index, quantity in order:
        product = all_products[index].name()
        if product in order_dict:
            order_dict[product] += quantity
        else:
            order_dict[product] = quantity
    ordered_products = "\n".join(f'\t{quantity} items: {product}'
                                 for product, quantity in order_dict.items())
    print(f"\033[0;32mOrder made! You've ordered: \n{ordered_products}\n"
          f"Total payment: ${total_price}\033[00m")


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
        func_key = ask_user_function_numer(func_dict)
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
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]
    best_buy = store.Store(product_list)

    # running dispatcher function
    start(best_buy)


if __name__ == "__main__":
    main()
