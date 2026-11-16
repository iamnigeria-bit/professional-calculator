
"""Calculation record and the calculation execution strategy."""

from dataclasses import dataclass
from datetime import datetime, timezone

from .calculator_config import CalculatorConfig
from .operations import OperationFactory
from .input_validators import finite_input, finite_number


@dataclass(frozen=True)
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str

    @classmethod
    def perform(cls, operation, left, right):
        """Run an operation using validated inputs."""

        config = CalculatorConfig.from_env()

        a = finite_input(left, config.max_input_value)
        b = finite_input(right, config.max_input_value)

        answer = finite_number(
            OperationFactory.create(operation).execute(a, b)
        )

        return cls(
            operation,
            a,
            b,
            answer,
            datetime.now(timezone.utc).isoformat()
        )
