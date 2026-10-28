import builtins

from app.calculator_config import CalculatorConfig
from app.calculator_repl import main


def test_new_operations_in_repl(monkeypatch, capsys, tmp_path):
    config = CalculatorConfig(
        tmp_path / "history.csv", False, 20
    )

    monkeypatch.setattr(
        "app.calculator_repl.CalculatorConfig.from_env",
        lambda: config,
    )

    answers = iter([
        "modulus", "10", "3",
        "int_divide", "10", "3",
        "percent", "25", "100",
        "abs_diff", "10", "3",
        "exit",
    ])

    monkeypatch.setattr(
        builtins, "input", lambda _: next(answers)
    )

    main()
    output = capsys.readouterr().out

    assert "Result: 1.0" in output
    assert "Result: 3.0" in output
    assert "Result: 25.0" in output
    assert "Result: 7.0" in output