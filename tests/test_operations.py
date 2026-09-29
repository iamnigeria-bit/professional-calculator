"""Tests for arithmetic operations."""

import pytest

from app.operation import add, subtract, multiply, divide


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        (add, 2, 3, 5),
        (add, -2, 2, 0),
        (add, 0, 0, 0),
        (add, 0.1, 0.2, 0.3),
        (subtract, 10, 4, 6),
        (subtract, 3, 5, -2),
        (subtract, -3, -2, -1),
        (subtract, 2.5, 1.2, 1.3),
        (multiply, 3, 4, 12),
        (multiply, 5, 0, 0),
        (multiply, -3, 4, -12),
        (multiply, 1.5, 2, 3),
        (divide, 10, 2, 5),
        (divide, 5, 2, 2.5),
        (divide, -6, 2, -3),
        (divide, 0, 5, 0),
    ],
)
def test_operations(operation, a, b, expected):
    """Check each operation with several number combinations."""
    assert operation(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("numerator", [10, 0, -5])
def test_divide_by_zero(numerator):
    """Verify that division by zero raises a helpful error."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(numerator, 0)