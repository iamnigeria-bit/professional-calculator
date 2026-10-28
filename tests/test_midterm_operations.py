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

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (25, 100, 25),
        (50, 200, 25),
        (30, 60, 50),
        (0, 75, 0),
    ],
)
def test_percentage(a, b, expected):
    operation = OperationFactory.create("percentage")
    assert operation.execute(a, b) == pytest.approx(expected)


def test_percentage_alias():
    operation = OperationFactory.create("percent")
    assert operation.execute(75, 300) == pytest.approx(25)

def test_percentage_by_zero():
    operation = OperationFactory.create("percentage")
    with pytest.raises(OperationError):
        operation.execute(25, 0)