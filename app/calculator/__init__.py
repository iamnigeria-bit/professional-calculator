"""Interactive calculator with session history."""

from app.calculation import CalculationFactory


class Calculator:
    """Manage user interaction and successful calculations."""

    def __init__(self):
        self.history = []

    def show_help(self):
        """Display available operations and commands."""
        print("Choose +, -, *, or /, then enter two numbers.")
        print("Commands: help, history, exit")
        print("Press Ctrl+C at any prompt to quit.")

    def show_history(self):
        """Display calculations from the current session."""
        if not self.history:
            print("No calculations yet.")
            return

        for number, (calculation, result) in enumerate(
            self.history, start=1
        ):
            print(f"{number}. {calculation} = {result}")

    def calculate(self, symbol, first, second):
        """Perform a calculation and save it if successful."""
        calculation = CalculationFactory.create(
            symbol, first, second
        )
        result = calculation.execute()
        self.history.append((calculation, result))
        return result

    def run(self):
        """Keep accepting commands until the user exits."""
        print("Welcome to the Professional Calculator!")
        self.show_help()

        while True:
            try:
                command = input("\nOperation or command: ").strip().lower()

                if command == "exit":
                    print("Goodbye!")
                    return

                if command == "help":
                    self.show_help()
                    continue

                if command == "history":
                    self.show_history()
                    continue

                if command not in CalculationFactory.operations:
                    print("Unknown command. Type 'help' for instructions.")
                    continue

                first = input("First number: ")
                second = input("Second number: ")
                result = self.calculate(command, first, second)
                print(f"Result: {result}")

            except ValueError as error:
                print(f"Error: {error}")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                return