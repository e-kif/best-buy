import pytest

from products import Product


def test_product_init():
    # Test that Product creation makes a class Product object
    assert isinstance(Product("MacBook Air M2", price=1200, quantity=12), Product), "Valid Product isn't created"


def test_empty_name():
    # Test that Product creation with empty name raises exception
    with pytest.raises(ValueError, match='Product name can not be empty.'):
        Product("", price=1450, quantity=100)


def test_negative_price():
    # Test that Product creation with negative price raises exception
    with pytest.raises(ValueError, match='Price should be a positive number.'):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_negative_quantity():
    # Test that Product creation with negative quantity raises exception
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("MacBook Air M2", price=144, quantity=-12.3)


def test_float_quantity():
    # Test that Product creation with a float quantity raises exception
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("Macbook Air M2", price=144, quantity=20.4)


def test_product_becomes_inactive():
    # Test that when a product reaches 0 quantity, it becomes inactive
    mac = Product("Macbook Air M2", price=1212, quantity=2)
    mac.set_quantity(0)
    assert not mac.is_active(), "Product didn't become inactive when reaches 0 quantity"


def test_product_buy():
    # Test that product purchase modifies the quantity and returns the right output.
    price = 1212
    quantity = 28
    buy = 11
    mac = Product("Macbook Air M2", price=price, quantity=quantity)
    assert mac.buy(11) == price*buy, "Order price calculated wrong"
    assert mac.get_quantity() == quantity - buy, "Product purchase results in wrong quantity left"


def test_buy_too_many():
    # Test that buying a larger quantity than exists invokes exception.
    quantity = 212
    mac = Product("Macbook Air M2", price=1212, quantity=quantity)
    with pytest.raises(ValueError, match='Quantity can not be bigger than items in store'):
        mac.buy(quantity + 1)
