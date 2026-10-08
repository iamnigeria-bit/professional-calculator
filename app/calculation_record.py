"""Calculation record and the calculation execution strategy."""
from dataclasses import dataclass
from datetime import datetime, timezone
from .operations import OperationFactory
from .input_validators import finite_number

@dataclass(frozen=True)
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str

    @classmethod
    def perform(cls, operation, left, right):
        """Run the selected strategy and create an immutable record."""
        a, b = finite_number(left), finite_number(right)
        answer = finite_number(OperationFactory.create(operation).execute(a, b))
        return cls(operation, a, b, answer, datetime.now(timezone.utc).isoformat())
