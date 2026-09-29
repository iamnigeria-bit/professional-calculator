"""Basic arithmetic operations for the calculator."""


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Subtract the second number from the first."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Divide two numbers, rejecting division by zero."""
    # LBYL: Check the denominator before attempting division.
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b