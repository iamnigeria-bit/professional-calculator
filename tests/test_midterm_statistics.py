
"""Tests for the optional calculation statistics feature."""

from app.calculation_record import Calculation
from app.calculator_repl import main
from app.history import History


def make_record(result):
    """Create a calculation record for testing."""
    return Calculation(
        operation="add",
        a=0.0,
        b=0.0,
        result=float(result),
        timestamp="2026-11-16T00:00:00Z",
    )


def test_statistics_empty_history():
    history = History()

    assert history.statistics() is None


def test_statistics_multiple_calculations():
    history = History()

    history.append(make_record(10))
    history.append(make_record(20))
    history.append(make_record(30))

    stats = history.statistics()

    assert stats["count"] == 3
    assert stats["average"] == 20.0
    assert stats["minimum"] == 10.0
    assert stats["maximum"] == 30.0


def test_statistics_single_calculation():
    history = History()

    history.append(make_record(15))

    stats = history.statistics()

    assert stats["count"] == 1
    assert stats["average"] == 15.0
    assert stats["minimum"] == 15.0
    assert stats["maximum"] == 15.0


def test_statistics_respects_history_limit():
    history = History(limit=2)

    history.append(make_record(10))
    history.append(make_record(20))
    history.append(make_record(30))

    stats = history.statistics()

    assert stats["count"] == 2
    assert stats["average"] == 25.0
    assert stats["minimum"] == 20.0
    assert stats["maximum"] == 30.0


def test_stats_command_in_repl(
    monkeypatch, capsys, tmp_path
):
    """Check statistics before and after a calculation."""

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(tmp_path / "stats_test.csv"),
    )
    monkeypatch.setenv(
        "CALCULATOR_LOG_DIR",
        str(tmp_path / "logs"),
    )
    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "false",
    )
    monkeypatch.setenv(
        "CALCULATOR_PRECISION",
        "2",
    )

    responses = iter([
        "stats",
        "add",
        "2",
        "8",
        "stats",
        "exit",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses),
    )

    main()

    output = capsys.readouterr().out

    assert "No calculations in history." in output
    assert "Calculation Statistics" in output
    assert "Total calculations: 1" in output
    assert "Average result: 10.00" in output
    assert "Minimum result: 10.00" in output
    assert "Maximum result: 10.00" in output
