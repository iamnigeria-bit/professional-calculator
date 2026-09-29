"""Calculation objects and the factory that creates them."""

import math

from app.operation import add, subtract, multiply, divide


class Calculation:
    """Store two numbers and the operation to perform."""

    def __init__(self, a, b, operation, symbol):
        self.a = a
        self.b = b
        self.operation = operation
        self.symbol = symbol

    def execute(self):
        """Calculate the result and reject overflow."""
        result = self.operation(self.a, self.b)
        if not math.isfinite(result):
            raise ValueError("Result is too large.")
        return result

    def __str__(self):
        """Return a readable description for calculation history."""
        return f"{self.a} {self.symbol} {self.b}"


class CalculationFactory:
    """Create calculations from an operation and two inputs."""

    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }

    @classmethod
    def create(cls, symbol, a, b):
        """Validate inputs and return a Calculation object."""
        # LBYL: Check whether the operation is supported.
        if symbol not in cls.operations:
            raise ValueError("Choose +, -, *, or /.")

        # EAFP: Attempt conversion, then handle invalid input.
        try:
            first = float(a)
            second = float(b)
        except (ValueError, TypeError, OverflowError) as error:
            raise ValueError("Please enter valid numbers.") from error

        if not math.isfinite(first) or not math.isfinite(second):
            raise ValueError("Numbers must be finite.")

        return Calculation(first, second, cls.operations[symbol], symbol)