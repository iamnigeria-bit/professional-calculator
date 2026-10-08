"""Input checks used at the REPL boundary (LBYL)."""
import math
from .exceptions import CalculatorError

def finite_number(value):
    """Convert input to float and reject NaN and infinity."""
    try:  # EAFP: ask conversion to perform the validation
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise CalculatorError("Enter a numeric value.") from exc
    if not math.isfinite(result):  # LBYL: check before calculation
        raise CalculatorError("Numbers must be finite.")
    return result
