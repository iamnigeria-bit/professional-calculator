
"""Input validation for the calculator."""

import math

from .exceptions import CalculatorError


def finite_number(value):
    """Convert a value to a finite float."""
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise CalculatorError(
            "Enter a numeric value."
        ) from exc

    if not math.isfinite(result):
        raise CalculatorError(
            "Numbers must be finite."
        )

    return result


def finite_input(value, max_input_value):
    """Validate input against the configured limit."""
    number = finite_number(value)

    if abs(number) > max_input_value:
        raise CalculatorError(
            f"Input must be between "
            f"-{max_input_value:g} and "
            f"{max_input_value:g}."
        )

    return number
