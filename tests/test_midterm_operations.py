import pytest

from app.operations import OperationFactory
from app.exceptions import OperationError


def test_modulus():
    operation = OperationFactory.create("modulus")
    assert operation.execute(10, 3) == 1


def test_modulus_alias():
    operation = OperationFactory.create("mod")
    assert operation.execute(11, 4) == 3


def test_modulus_by_zero():
    operation = OperationFactory.create("modulus")
    with pytest.raises(OperationError):
        operation.execute(10, 0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 3),
        (-7, 2, -3),
        (7, -2, -3),
        (0, 5, 0),
    ],
)
def test_integer_division(a, b, expected):
    operation = OperationFactory.create("int_divide")
    assert operation.execute(a, b) == expected


def test_integer_division_alias():
    operation = OperationFactory.create("integer_division")
    assert operation.execute(15, 4) == 3


def test_integer_division_by_zero():
    operation = OperationFactory.create("int_divide")
    with pytest.raises(OperationError):
        operation.execute(10, 0)