"""Tests for calculation objects and input validation."""

import pytest

from app.calculation import Calculation, CalculationFactory


@pytest.mark.parametrize(
    "symbol, a, b, expected",
    [
        ("+", 2, 3, 5),
        ("-", 3, 5, -2),
        ("*", -3, 4, -12),
        ("/", 5, 2, 2.5),
        ("+", "2.5", "3.5", 6),
        ("+", 0.1, 0.2, 0.3),
    ],
)
def test_create_calculation(symbol, a, b, expected):
    """Create calculations and verify their results."""
    calculation = CalculationFactory.create(symbol, a, b)

    assert isinstance(calculation, Calculation)
    assert calculation.execute() == pytest.approx(expected)


def test_calculation_description():
    """Check the text used to display a calculation."""
    calculation = CalculationFactory.create("+", 2, 3)

    assert str(calculation) == "2.0 + 3.0"


@pytest.mark.parametrize("symbol", ["%", "", "add"])
def test_invalid_operation(symbol):
    """Reject unsupported operations."""
    with pytest.raises(ValueError, match="Choose"):
        CalculationFactory.create(symbol, 2, 3)


@pytest.mark.parametrize(
    "a, b",
    [
        ("hello", 2),
        (2, "hello"),
        ("", 2),
        (None, 2),
        (2, None),
        (10**400, 2),
        (2, 10**400),
    ],
)
def test_invalid_numbers(a, b):
    """Reject inputs that cannot be converted to numbers."""
    with pytest.raises(ValueError, match="Please enter valid numbers"):
        CalculationFactory.create("+", a, b)


@pytest.mark.parametrize(
    "a, b",
    [
        ("nan", 2),
        (2, "nan"),
        ("inf", 2),
        (2, "inf"),
        ("-inf", 2),
        (2, "-inf"),
    ],
)
def test_nonfinite_numbers(a, b):
    """Reject infinity and not-a-number inputs."""
    with pytest.raises(ValueError, match="Numbers must be finite"):
        CalculationFactory.create("+", a, b)


@pytest.mark.parametrize(
    "symbol, a, b",
    [
        ("+", 1e308, 1e308),
        ("-", -1e308, 1e308),
        ("*", 1e308, 10),
        ("/", 1e308, 1e-308),
    ],
)
def test_result_overflow(symbol, a, b):
    """Reject results that exceed the supported numeric range."""
    calculation = CalculationFactory.create(symbol, a, b)

    with pytest.raises(ValueError, match="Result is too large"):
        calculation.execute()


def test_calculation_divide_by_zero():
    """Verify division errors reach the caller."""
    calculation = CalculationFactory.create("/", 10, 0)

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation.execute()