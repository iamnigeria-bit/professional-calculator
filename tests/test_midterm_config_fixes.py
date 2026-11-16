
"""Regression tests for midterm configuration fixes."""

import pytest

from app.calculation_record import Calculation
from app.calculator_repl import Calculator, main
from app.exceptions import CalculatorError


@pytest.mark.parametrize("value", [11, -11])
def test_maximum_input_rejected(monkeypatch, value):
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "10")

    with pytest.raises(CalculatorError):
        Calculation.perform("add", value, 1)


def test_valid_inputs_can_produce_larger_result(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "10")

    result = Calculation.perform("add", 10, 5)

    assert result.result == 15


def test_configured_decimal_precision(
    monkeypatch, capsys, tmp_path
):
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path))

    responses = iter(["/", "1", "3", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    main()

    output = capsys.readouterr().out
    assert "Result: 0.3333" in output


def test_history_directory_and_encoding(
    monkeypatch, tmp_path
):
    history_dir = tmp_path / "custom_history"

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_DIR",
        str(history_dir)
    )
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        "history.csv"
    )
    monkeypatch.setenv(
        "CALCULATOR_DEFAULT_ENCODING",
        "utf-16"
    )
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    monkeypatch.setenv(
        "CALCULATOR_LOG_DIR",
        str(tmp_path / "logs")
    )

    calculator = Calculator(load_existing=False)
    calculator.calculate("add", 10, 5)

    history_file = history_dir / "history.csv"

    assert history_file.exists()

    # UTF-16 files should begin with a byte-order mark.
    assert history_file.read_bytes().startswith(
        (b"\xff\xfe", b"\xfe\xff")
    )

    restored = Calculator(load_existing=True)

    assert len(restored.history.entries) == 1
    assert restored.history.entries[0].result == 15
