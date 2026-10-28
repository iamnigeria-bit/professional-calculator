from types import SimpleNamespace

from app.calculator_repl import LoggingObserver


def test_logging_observer_writes_calculation(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", "calculator.log")

    observer = LoggingObserver()
    calculation = SimpleNamespace(
        operation="modulus", a=10, b=3, result=1
    )

    observer.update(calculation, None)

    for handler in observer.logger.handlers:
        handler.flush()

    log_file = tmp_path / "calculator.log"
    content = log_file.read_text(encoding="utf-8")

    assert "operation=modulus" in content
    assert "a=10" in content
    assert "b=3" in content
    assert "result=1" in content