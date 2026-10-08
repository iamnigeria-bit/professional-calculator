"""Tests for the calculator's interactive interface."""

import runpy

import pytest

from calculator.cli import main, read_number


def provide_inputs(monkeypatch, answers):
    """Supply answers automatically instead of typing them."""
    responses = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))


@pytest.mark.parametrize(
    "operation,first,second,expected",
    [
        ("+", "2", "3", "5.0"),
        ("-", "10", "4", "6.0"),
        ("*", "3", "4", "12.0"),
        ("/", "5", "2", "2.5"),
    ],
)
def test_calculation(monkeypatch, capsys, operation, first, second, expected):
    provide_inputs(monkeypatch, [operation, first, second, "exit"])

    main()

    output = capsys.readouterr().out
    assert f"Result: {expected}" in output
    assert "Goodbye!" in output


def test_multiple_calculations(monkeypatch, capsys):
    provide_inputs(
        monkeypatch,
        ["+", "2", "3", "*", "4", "5", "exit"],
    )

    main()

    output = capsys.readouterr().out
    assert "Result: 5.0" in output
    assert "Result: 20.0" in output


def test_invalid_operation(monkeypatch, capsys):
    provide_inputs(monkeypatch, ["invalid", "+", "2", "3", "exit"])

    main()

    output = capsys.readouterr().out
    assert "Invalid operation" in output
    assert "Result: 5.0" in output


@pytest.mark.parametrize("invalid", ["hello", "", "nan", "inf", "-inf", "1e999"])
def test_invalid_number(monkeypatch, capsys, invalid):
    provide_inputs(monkeypatch, [invalid, "2.5"])

    result = read_number("Number: ")

    assert result == 2.5
    assert "Please enter a valid, finite number" in capsys.readouterr().out


@pytest.mark.parametrize(
    "answers,message",
    [
        (["/", "10", "0"], "Cannot divide by zero."),
        (["*", "1e308", "1e308"], "Result is too large to represent."),
    ],
)
def test_error_recovery(monkeypatch, capsys, answers, message):
    provide_inputs(monkeypatch, answers + ["+", "2", "3", "exit"])

    main()

    output = capsys.readouterr().out
    assert f"Error: {message}" in output
    assert "Result: 5.0" in output


def test_exit_with_spaces_and_capitals(monkeypatch, capsys):
    provide_inputs(monkeypatch, ["  EXIT  "])

    main()

    assert "Goodbye!" in capsys.readouterr().out


@pytest.mark.parametrize("exception", [EOFError, KeyboardInterrupt])
@pytest.mark.parametrize("answers", [[], ["+"], ["+", "2"]])
def test_interrupted_input(monkeypatch, capsys, exception, answers):
    responses = iter(answers)

    def interrupted_input(prompt):
        try:
            return next(responses)
        except StopIteration:
            raise exception

    monkeypatch.setattr("builtins.input", interrupted_input)

    main()

    assert "Goodbye!" in capsys.readouterr().out


def test_module_startup(monkeypatch, capsys):
    provide_inputs(monkeypatch, ["exit"])

    runpy.run_module("calculator", run_name="__main__")

    output = capsys.readouterr().out
    assert "Welcome to the calculator!" in output
    assert "Goodbye!" in output