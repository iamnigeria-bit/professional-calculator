# Professional Calculator

A Python command-line calculator with arithmetic operations,
input validation, and calculation history.

## Features

- Addition, subtraction, multiplication, and division
- Continuous interaction through a Read-Eval-Print Loop (REPL)
- Help and calculation history commands
- Helpful messages for invalid input and division by zero
- Validation for nonfinite numbers and overflowing results
- Clean exit using the exit command, Ctrl+C, or end-of-input

## Setup

From the project directory, create and activate a virtual environment.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the testing dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Calculator

```bash
python -m app
```

Enter an operation: +, -, *, or /.
Then enter the first and second numbers when prompted.

Example:

```text
Operation or command: +
First number: 2
Second number: 3
Result: 5.0
```

Available commands:

- help: Display instructions.
- history: Display successful calculations from this session.
- exit: Close the calculator.

History is stored in memory and is cleared when the program closes.
At a number prompt, use Ctrl+C to quit.

## Project Organization

- app/operation/__init__.py: Arithmetic functions.
- app/calculation/__init__.py: Calculation and CalculationFactory classes.
- app/calculator/__init__.py: User interaction and session history.
- app/__main__.py: Application entry point.
- tests/test_operations.py: Parameterized arithmetic tests.
- tests/test_calculations.py: Calculation and validation tests.
- tests/test_calculator.py: Interaction, history, and error-recovery tests.

## Design

The Calculation class stores the operands and operation.
CalculationFactory validates inputs and creates Calculation objects.
The Calculator class manages prompts, results, and history.

Arithmetic functions are reused instead of duplicated, following
the Don't Repeat Yourself (DRY) principle.

### Error Handling

Look Before You Leap (LBYL) is used to check supported operations
and reject division by zero before attempting the calculation.

Easier to Ask Forgiveness than Permission (EAFP) is used when
converting inputs to numbers. The program attempts conversion
and catches conversion errors.

Invalid calculations display helpful messages and are not added
to history. Users can continue calculating after an error.

## Testing

Run all tests:

```bash
python -m pytest
```

Check line and branch coverage and require 100%:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=100
```

The test suite includes parameterized cases for arithmetic,
invalid inputs, division by zero, and numeric overflow.
Mocked input simulates user interaction and interruptions.

Local verification: 74 tests passed with 100% line and branch coverage.

### Coverage Exclusions

The comment `# pragma: no cover` can exclude a line or clause
from coverage measurement. Exclusions should be justified rather
than used to hide untested application behavior.

This project does not need coverage exclusions. Its entry point,
interactive prompts, and error handling are exercised by tests.

## Numeric Limitations

The calculator uses Python floating-point numbers. Some decimal
results may have small rounding differences. Tests use
pytest.approx when comparing calculated numeric results.