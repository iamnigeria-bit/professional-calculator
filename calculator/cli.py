"""Interactive command-line calculator."""

import math

from calculator.operations import add, subtract, multiply, divide


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def read_number(prompt):
    """Keep asking until the user enters a finite number."""
    while True:
        try:
            number = float(input(prompt))
            if not math.isfinite(number):
                raise ValueError
            return number
        except ValueError:
            print("Please enter a valid, finite number, such as 5 or -2.5.")


def main():
    """Run the calculator until the user exits."""
    print("Welcome to the calculator!")
    print("Choose +, -, *, or /. Type 'exit' to quit.")
    print("You can also press Ctrl+C at any prompt to quit.")

    while True:
        try:
            operation = input("\nOperation: ").strip().lower()

            if operation == "exit":
                print("Goodbye!")
                break

            if operation not in OPERATIONS:
                print("Invalid operation. Choose +, -, *, or /.")
                continue

            first = read_number("First number: ")
            second = read_number("Second number: ")

            try:
                result = OPERATIONS[operation](first, second)
                if not math.isfinite(result):
                    raise ValueError("Result is too large to represent.")
                print(f"Result: {result}")
            except ValueError as error:
                print(f"Error: {error}")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break