
"""DataFrame-backed, persistable calculation history."""

from pathlib import Path

import pandas as pd

from .calculation_record import Calculation
from .exceptions import CalculatorError


COLUMNS = ["operation", "a", "b", "result", "timestamp"]


class History:
    """Store, analyze, save, and load calculation history."""

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

    def statistics(self):
        """Return summary statistics for calculation results."""

        if not self.entries:
            return None

        frame = self.dataframe()
        results = frame["result"]

        return {
            "count": len(results),
            "average": float(results.mean()),
            "minimum": float(results.min()),
            "maximum": float(results.max()),
        }

    def save(self, filename, encoding="utf-8"):
        path = Path(filename)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

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
            pd.errors.EmptyDataError,
        ) as exc:
            raise CalculatorError(
                f"Cannot load history: {exc}"
            ) from exc

        self.entries = entries[-self.limit:]
        return True
