# Command-Line Calculator

A Python calculator that runs in the terminal. It uses a
Read-Eval-Print Loop (REPL), allowing users to perform multiple
calculations until they choose to exit.

## Features

- Addition, subtraction, multiplication, and division
- Support for negative numbers and decimals
- Input validation with helpful error messages
- Division-by-zero handling
- Rejection of infinite numbers, NaN, and nonfinite results
- Automated tests with 100% statement and branch coverage

## Setup

This project was tested locally with Python 3.9.6.

Clone the repository and enter the project folder:

```bash
git clone https://github.com/iamnigeria-bit/command-line-calculator.git
cd command-line-calculator
```

Create and activate a virtual environment on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the testing dependencies:

```bash
python -m pip install -r requirements.txt
```

Activate the virtual environment again whenever you open a new
terminal session.

## Run the Calculator

From the project folder, run:

```bash
python -m calculator
```

Enter an operation: +, -, *, or /. Then enter the two numbers
when prompted.

Example:

```text
Operation: +
First number: 2
Second number: 3
Result: 5.0
```

The calculator asks for another operation after each calculation.
Type `exit` at the operation prompt to quit, or press Ctrl+C at
any prompt.

Invalid numbers trigger another number prompt. Invalid operations,
division by zero, and nonfinite results display an error message
without closing the calculator.

## Project Organization

- `calculator/operations.py`: arithmetic functions
- `calculator/cli.py`: prompts, validation, and the REPL
- `calculator/__main__.py`: starts the application
- `calculator/__init__.py`: marks the calculator package
- `tests/test_operations.py`: parameterized arithmetic tests
- `tests/test_cli.py`: interaction, error recovery, and startup tests
- `.github/workflows/tests.yml`: automated testing workflow
- `requirements.txt`: testing dependencies

Arithmetic is separated from user interaction. A shared number-reading
function and an operation dictionary reduce repeated code.

## Testing

Run all tests:

```bash
python -m pytest -v
```

Run tests with statement and branch coverage, requiring 100%:

```bash
python -m pytest --cov=calculator --cov-branch --cov-report=term-missing --cov-fail-under=100
```

The current suite contains 41 passing tests. It checks arithmetic,
invalid input, division by zero, oversized results, repeated
calculations, quitting, interrupted input, and module startup.

Coverage measures which code paths the tests execute; it does not
guarantee that every possible bug has been eliminated.

## Continuous Integration

The GitHub Actions workflow runs on pushes and pull requests.
It installs the dependencies and runs the tests with coverage.

The workflow fails if any test fails or if coverage falls below 100%.
---

## Module 5 — Enhanced calculator (new `app/` package)

This project preserves the original `calculator/` application and its tests, while adding
an enhanced modular implementation in `app/` following the assignment's requested structure.

### Install and run

Use Python 3.9 or newer. From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate         # on Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m app
```

Enter an operation followed by two numbers. Available operations:
`+`, `-`, `*`, `/`, `^`, `root`, and the word equivalents (`add`, `subtract`,
`multiply`, `divide`, `power`). `root` takes the radicand first and the degree second:
`root(27, 3)` returns `3.0`. Negative radicands are supported for odd integer degrees.
Complex results and non-finite inputs are rejected.

Commands: `help`, `history`, `clear`, `undo`, `redo`, `save`, `load`, `exit`.
The calculation history is stored as a pandas DataFrame and auto-saved to CSV by default.
Undo and redo restore prior **history states**; new calculations clear the redo stack.

### Settings

Copy `.env.example` to `.env` to customize:

- `CALC_HISTORY_FILE`: CSV path (default `calculator_history.csv`)
- `CALC_AUTO_SAVE`: `true` or `false` (default `true`)
- `CALC_MAX_HISTORY`: positive integer (default `1000`)

The `.env` file is ignored by Git; CSV history files are ignored by default.

### Design patterns and modules

- **Strategy**: `app/operations.py` operation subclasses implement `execute`.
- **Factory**: `OperationFactory.create()` selects a strategy from input.
- **Observer**: `HistoryObserver` and `AutoSaveObserver` respond to successful calculations.
- **Memento**: `Caretaker` stores history snapshots for undo and redo.
- **Facade**: `Calculator` offers a simplified API for these subsystems.
- `app/calculation.py`: immutable calculation records.
- `app/calculator_config.py`: environment settings and validation.
- `app/history.py`: pandas DataFrame/CSV persistence.
- `app/input_validators.py`: finite-number checks, LBYL and EAFP demonstrations.
- `app/exceptions.py`: domain errors.
- `app/calculator_repl.py`: interactive command-line application.

### Tests and continuous integration

```bash
python -m pytest tests/ --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=100
```

The workflow at `.github/workflows/python-app.yml` runs all old and new tests
and requires **100% statement and branch coverage of the new `app/` package**.
The legacy `calculator/` package is still tested, but is not included in the
new-app coverage denominator.

### GitHub submission

Push this project to your existing repository and submit the GitHub repository URL
in Canvas. Before pushing, run the tests locally and inspect the GitHub Actions run.
