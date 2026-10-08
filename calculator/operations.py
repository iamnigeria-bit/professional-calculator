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
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def power(a, b):
    """Raise a number to a specified power."""
    return a ** b


def root(a, b):
    """Calculate the b-th root of a."""
    if b == 0:
        raise ValueError("Root degree cannot be zero.")

    if a < 0:
        if not float(b).is_integer() or int(b) % 2 == 0:
            raise ValueError(
                "Negative numbers require an odd integer root."
            )
        return -((-a) ** (1 / int(b)))

    return a ** (1 / b)
