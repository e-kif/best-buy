import pytest

from products import Product


def test_empty_name():
    # Empty name
    with pytest.raises(ValueError, match='Product name can not be empty.'):
        Product("", price=1450, quantity=100)


def test_negative_price():
    # Negative Price
    with pytest.raises(ValueError, match='Price should be a positive number.'):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_negative_quantity():
    # Negative quantity
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("MacBook Air M2", price=144, quantity=-12.3)


def test_float_quantity():
    # Quantity is a float
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("Macbook Air M2", price=144, quantity=20.4)