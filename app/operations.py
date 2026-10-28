"""Operation strategies and their factory."""
from abc import ABC, abstractmethod
from .exceptions import OperationError
from .input_validators import finite_number

class Operation(ABC):
    """Strategy interface for a two-operand calculation."""
    @abstractmethod
    def execute(self, a, b):
        """Compute the result."""

class Add(Operation):
    def execute(self, a, b):
        return a + b

class Subtract(Operation):
    def execute(self, a, b):
        return a - b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b

class Power(Operation):
    def execute(self, a, b):
        try:
            value = a ** b
        except (OverflowError, ZeroDivisionError) as exc:
            raise OperationError("Invalid power calculation.") from exc
        if isinstance(value, complex):
            raise OperationError("Complex results are not supported.")
        return finite_number(value)

class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Root degree cannot be zero.")
        if a < 0:
            if not float(b).is_integer() or int(b) % 2 == 0:
                raise OperationError("Negative values need an odd integer root degree.")
            if a == -1:
                return -1.0
            return -((-a) ** (1 / b))
        try:
            return a ** (1 / b)
        except (OverflowError, ZeroDivisionError) as exc:
            raise OperationError("Invalid root calculation.") from exc
class Modulus(Operation):
    """Calculate the remainder after division."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot calculate modulus by zero.")
        return a % b

class IntegerDivision(Operation):
    """Divide two numbers and discard the fractional part."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return int(a / b)

class Percentage(Operation):
    """Calculate a as a percentage of b."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot calculate percentage with a zero denominator.")
        return (a / b) * 100

class AbsoluteDifference(Operation):
    """Calculate the absolute difference between two numbers."""

    def execute(self, a, b):
        return abs(a - b)

class OperationFactory:
    """Factory maps symbols/words to interchangeable strategies."""
    _strategies = {"modulus": Modulus,
"mod": Modulus, 
"percentage": Percentage,
"percent": Percentage,
"int_divide": IntegerDivision,
"integer_division": IntegerDivision,
"abs_diff": AbsoluteDifference,
"absolute_difference": AbsoluteDifference,
        "+": Add, "add": Add, "-": Subtract, "subtract": Subtract,
        "*": Multiply, "multiply": Multiply, "/": Divide, "divide": Divide,
        "^": Power, "power": Power, "root": Root,
    }

    @classmethod
    def create(cls, operation):
        try:
            return cls._strategies[operation.lower()]()
        except (KeyError, AttributeError) as exc:
            raise OperationError(f"Unsupported operation: {operation}") from exc
