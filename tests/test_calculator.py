"""Tests for the interactive calculator."""

import runpy
from unittest.mock import Mock

import pytest

from app.calculator import Calculator


def test_empty_history(capsys):
    """Show a helpful message when history is empty."""
    calculator = Calculator()
    calculator.show_history()

    assert "No calculations yet." in capsys.readouterr().out


def test_saved_history(capsys):
    """Save successful calculations in order."""
    calculator = Calculator()

    assert calculator.calculate("+", "2", "3") == 5
    assert calculator.calculate("*", "4", "5") == 20

    calculator.show_history()
    output = capsys.readouterr().out

    assert len(calculator.history) == 2
    assert "1. 2.0 + 3.0 = 5.0" in output
    assert "2. 4.0 * 5.0 = 20.0" in output


def test_separate_histories():
    """Each calculator has its own history."""
    first = Calculator()
    second = Calculator()

    first.calculate("+", 2, 3)

    assert len(first.history) == 1
    assert second.history == []


@pytest.mark.parametrize(
    "symbol, a, b",
    [
        ("/", 2, 0),
        ("+", "hello", 2),
        ("%", 2, 3),
        ("*", 1e308, 10),
    ],
)
def test_failed_calculation_not_saved(symbol, a, b):
    """Failed calculations do not change existing history."""
    calculator = Calculator()
    calculator.calculate("+", 2, 3)
    original_history = calculator.history.copy()

    with pytest.raises(ValueError):
        calculator.calculate(symbol, a, b)

    assert calculator.history == original_history


def test_help(capsys):
    """Explain operations and available commands."""
    Calculator().show_help()
    output = capsys.readouterr().out

    assert "Choose +, -, *, or /" in output
    assert "Commands: help, history, exit" in output
    assert "Ctrl+C" in output


@pytest.mark.parametrize(
    "symbol, a, b, expected",
    [
        ("+", "2", "3", "5.0"),
        ("-", "3", "5", "-2.0"),
        ("*", "4", "5", "20.0"),
        ("/", "5", "2", "2.5"),
    ],
)
def test_interactive_operations(monkeypatch, capsys, symbol, a, b, expected):
    """Accept an operation and two numbers, then exit."""
    simulated_input = Mock(side_effect=[symbol, a, b, "exit"])
    monkeypatch.setattr("builtins.input", simulated_input)

    calculator = Calculator()
    calculator.run()
    output = capsys.readouterr().out

    assert f"Result: {expected}" in output
    assert "Goodbye!" in output
    assert len(calculator.history) == 1


def test_interactive_commands(monkeypatch, capsys):
    """Handle help, empty history, and populated history."""
    simulated_input = Mock(
        side_effect=[
            " HELP ",
            "history",
            "+",
            "2",
            "3",
            " HISTORY ",
            " EXIT ",
        ]
    )
    monkeypatch.setattr("builtins.input", simulated_input)

    Calculator().run()
    output = capsys.readouterr().out

    assert output.count("Commands: help, history, exit") == 2
    assert "No calculations yet." in output
    assert "1. 2.0 + 3.0 = 5.0" in output
    assert "Goodbye!" in output


@pytest.mark.parametrize("command", ["unknown", "", "%"])
def test_unknown_command(monkeypatch, capsys, command):
    """Explain an unsupported command and continue."""
    monkeypatch.setattr(
        "builtins.input",
        Mock(side_effect=[command, "exit"]),
    )

    Calculator().run()
    output = capsys.readouterr().out

    assert "Unknown command." in output
    assert "Goodbye!" in output


@pytest.mark.parametrize(
    "symbol, a, b, message",
    [
        ("+", "hello", "2", "Please enter valid numbers."),
        ("/", "2", "0", "Cannot divide by zero."),
        ("+", "nan", "2", "Numbers must be finite."),
        ("*", "1e308", "10", "Result is too large."),
    ],
)
def test_recover_after_error(monkeypatch, capsys, symbol, a, b, message):
    """Allow another calculation after an error."""
    monkeypatch.setattr(
        "builtins.input",
        Mock(side_effect=[symbol, a, b, "+", "2", "3", "exit"]),
    )

    calculator = Calculator()
    calculator.run()
    output = capsys.readouterr().out

    assert f"Error: {message}" in output
    assert "Result: 5.0" in output
    assert len(calculator.history) == 1


@pytest.mark.parametrize("exception", [KeyboardInterrupt, EOFError])
@pytest.mark.parametrize("earlier_inputs", [[], ["+"], ["+", "2"]])
def test_interrupt_at_any_prompt(
    monkeypatch, capsys, exception, earlier_inputs
):
    """Exit cleanly if input is interrupted at any prompt."""
    monkeypatch.setattr(
        "builtins.input",
        Mock(side_effect=earlier_inputs + [exception()]),
    )

    calculator = Calculator()
    calculator.run()

    assert "Goodbye!" in capsys.readouterr().out
    assert calculator.history == []


def test_application_entry_point(monkeypatch, capsys):
    """Verify that running the app starts the calculator."""
    monkeypatch.setattr(
        "builtins.input",
        Mock(side_effect=["exit"]),
    )

    runpy.run_module("app", run_name="__main__")
    output = capsys.readouterr().out

    assert "Welcome to the Professional Calculator!" in output
    assert "Goodbye!" in output