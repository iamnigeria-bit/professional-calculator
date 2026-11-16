
"""Facade, observers, and interactive REPL entry point."""

import logging
import os
from pathlib import Path

from .calculator_config import CalculatorConfig
from .calculator_memento import Caretaker
from .calculation_record import Calculation
from .exceptions import CalculatorError
from .history import History


HELP = (
    "Commands: + - * / ^ root modulus int_divide percent abs_diff, "
    "history, clear, undo, redo, save, load, help, exit"
)


class HistoryObserver:
    """Record successful calculations in history."""

    def update(self, calculation, calculator):
        calculator.history.append(calculation)


class LoggingObserver:
    """Log successful calculations to a file."""

    def __init__(self):
        folder = Path(
            os.getenv("CALCULATOR_LOG_DIR", "logs")
        )

        filename = Path(
            os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
        )

        path = (
            filename
            if filename.is_absolute()
            else folder / filename
        )

        path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(
            f"calculator.{path.resolve()}"
        )

        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        if not self.logger.handlers:
            handler = logging.FileHandler(
                path,
                encoding=os.getenv(
                    "CALCULATOR_DEFAULT_ENCODING",
                    "utf-8"
                )
            )

            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s %(message)s"
                )
            )

            self.logger.addHandler(handler)

    def update(self, calculation, calculator):
        self.logger.info(
            "operation=%s a=%s b=%s result=%s",
            calculation.operation,
            calculation.a,
            calculation.b,
            calculation.result,
        )


class AutoSaveObserver:
    """Automatically save history when enabled."""

    def update(self, calculation, calculator):
        if calculator.config.auto_save:
            calculator.history.save(
                calculator.history_path,
                encoding=calculator.config.default_encoding
            )


class Calculator:
    """Coordinate operations, history, observers, and snapshots."""

    def __init__(self, config=None, load_existing=True):
        self.config = config or CalculatorConfig.from_env()

        # Resolve history file using the configured directory.
        history_file = Path(self.config.history_file)
        history_dir = Path(self.config.history_dir)

        self.history_path = (
            history_file
            if history_file.is_absolute()
            else history_dir / history_file
        )

        self.history = History(
            self.config.max_history
        )

        self.caretaker = Caretaker()

        self.observers = [
            HistoryObserver(),
            LoggingObserver(),
            AutoSaveObserver(),
        ]

        if load_existing:
            self.history.load(
                self.history_path,
                encoding=self.config.default_encoding
            )

    def calculate(self, operation, a, b):
        """Perform a calculation and notify observers."""

        record = Calculation.perform(
            operation,
            a,
            b
        )

        self.caretaker.remember(
            self.history.entries
        )

        for observer in self.observers:
            observer.update(
                record,
                self
            )

        return record.result

    def clear(self):
        """Clear calculation history."""

        self.caretaker.remember(
            self.history.entries
        )

        self.history.clear()
        self._save_if_enabled()

    def undo(self):
        """Undo the last history change."""

        self.history.entries = self.caretaker.undo(
            self.history.entries
        )

        self._save_if_enabled()

    def redo(self):
        """Redo the last undone history change."""

        self.history.entries = self.caretaker.redo(
            self.history.entries
        )

        self._save_if_enabled()

    def save(self):
        """Save history using configured directory and encoding."""

        self.history.save(
            self.history_path,
            encoding=self.config.default_encoding
        )

    def load(self):
        """Load history using configured directory and encoding."""

        snapshot = list(
            self.history.entries
        )

        if self.history.load(
            self.history_path,
            encoding=self.config.default_encoding
        ):
            self.caretaker.remember(snapshot)
            return True

        return False

    def _save_if_enabled(self):
        """Save history after changes when auto-save is enabled."""

        if self.config.auto_save:
            self.save()


def main():
    """Run the calculator's interactive command-line interface."""

    try:
        calculator = Calculator()

    except CalculatorError as exc:
        print(f"Configuration/history error: {exc}")
        return

    print(
        "Welcome to the Professional Calculator! "
        + HELP
    )

    while True:
        try:
            command = input(
                "Operation or command: "
            ).strip().lower()

            if command == "exit":
                print("Goodbye!")
                return

            if command == "help":
                print(HELP)

            elif command == "history":
                print(
                    calculator.history.dataframe().to_string(
                        index=False
                    )
                )

            elif command in {
                "clear",
                "undo",
                "redo",
                "save",
                "load",
            }:
                result = getattr(
                    calculator,
                    command
                )()

                if command == "load" and result is False:
                    print("No saved history file found.")
                else:
                    print(
                        f"{command.title()} complete."
                    )

            else:
                left = input("First number: ")
                right = input("Second number: ")

                result = calculator.calculate(
                    command,
                    left,
                    right
                )

                # Display the configured number of decimal places.
                print(
                    f"Result: {result:.{calculator.config.precision}f}"
                )

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return

        except CalculatorError as exc:
            LoggingObserver().logger.error(
                "Calculator error: %s",
                exc
            )

            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
