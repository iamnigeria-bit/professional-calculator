"""Facade, observers, and interactive REPL entry point."""
from .calculator_config import CalculatorConfig
from .calculator_memento import Caretaker
from .calculation_record import Calculation
from .exceptions import CalculatorError
from .history import History

HELP = "Commands: + - * / ^ root, history, clear, undo, redo, save, load, help, exit"

class HistoryObserver:
    """Observer automatically records successful calculations."""
    def update(self, calculation, calculator):
        calculator.history.append(calculation)

class AutoSaveObserver:
    """Observer persists successful calculations when enabled."""
    def update(self, calculation, calculator):
        if calculator.config.auto_save:
            calculator.history.save(calculator.config.history_file)

class Calculator:
    """Facade coordinating operations, history, observers and snapshots."""
    def __init__(self, config=None, load_existing=True):
        self.config = config or CalculatorConfig.from_env()
        self.history = History(self.config.max_history)
        self.caretaker = Caretaker()
        self.observers = [HistoryObserver(), AutoSaveObserver()]
        if load_existing:
            self.history.load(self.config.history_file)

    def calculate(self, operation, a, b):
        record = Calculation.perform(operation, a, b)
        self.caretaker.remember(self.history.entries)
        for observer in self.observers:
            observer.update(record, self)
        return record.result

    def clear(self):
        self.caretaker.remember(self.history.entries)
        self.history.clear()
        self._save_if_enabled()

    def undo(self):
        self.history.entries = self.caretaker.undo(self.history.entries)
        self._save_if_enabled()

    def redo(self):
        self.history.entries = self.caretaker.redo(self.history.entries)
        self._save_if_enabled()

    def save(self):
        self.history.save(self.config.history_file)

    def load(self):
        snapshot = list(self.history.entries)
        if self.history.load(self.config.history_file):
            self.caretaker.remember(snapshot)
            return True
        return False

    def _save_if_enabled(self):
        if self.config.auto_save:
            self.save()


def main():
    """Run the command-line REPL; errors stay inside the loop."""
    try:
        calculator = Calculator()
    except CalculatorError as exc:
        print(f"Configuration/history error: {exc}")
        return
    print("Welcome to the Professional Calculator! " + HELP)
    while True:
        try:
            command = input("Operation or command: ").strip().lower()
            if command == "exit":
                print("Goodbye!")
                return
            if command == "help":
                print(HELP)
            elif command == "history":
                print(calculator.history.dataframe().to_string(index=False))
            elif command in {"clear", "undo", "redo", "save", "load"}:
                result = getattr(calculator, command)()
                if command == "load" and result is False:
                    print("No saved history file found.")
                else:
                    print(f"{command.title()} complete.")
            else:
                left = input("First number: ")
                right = input("Second number: ")
                print(f"Result: {calculator.calculate(command, left, right)}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return
        except CalculatorError as exc:
            print(f"Error: {exc}")
