
"""DataFrame-backed, persistent calculation history."""

from pathlib import Path

import pandas as pd

from .calculation_record import Calculation
from .exceptions import CalculatorError


COLUMNS = ["operation", "a", "b", "result", "timestamp"]


class History:
    def __init__(self, limit=1000):
        self.limit = limit
        self.entries = []

    def append(self, entry):
        self.entries.append(entry)
        self.entries = self.entries[-self.limit:]

    def clear(self):
        self.entries.clear()

    def dataframe(self):
        return pd.DataFrame(
            [vars(entry) for entry in self.entries],
            columns=COLUMNS
        )

    def save(self, filename, encoding="utf-8"):
        """Save history using the configured encoding."""
        path = Path(filename)

        try:
            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.dataframe().to_csv(
                path,
                index=False,
                encoding=encoding
            )

        except (OSError, UnicodeError, LookupError) as exc:
            raise CalculatorError(
                f"Cannot save history: {exc}"
            ) from exc

    def load(self, filename, encoding="utf-8"):
        """Load and validate previously saved history."""
        path = Path(filename)

        if not path.is_file():
            return False

        try:
            frame = pd.read_csv(
                path,
                encoding=encoding
            )

            if list(frame.columns) != COLUMNS:
                raise CalculatorError(
                    "History CSV has invalid columns."
                )

            entries = [
                Calculation(
                    str(row.operation),
                    float(row.a),
                    float(row.b),
                    float(row.result),
                    str(row.timestamp)
                )
                for row in frame.itertuples(index=False)
            ]

        except (
            OSError,
            ValueError,
            TypeError,
            UnicodeError,
            LookupError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError
        ) as exc:
            raise CalculatorError(
                f"Cannot load history: {exc}"
            ) from exc

        self.entries = entries[-self.limit:]
        return True
