"""Validated environment-based configuration."""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from .exceptions import ConfigurationError

@dataclass(frozen=True)
class CalculatorConfig:
    history_file: Path
    auto_save: bool
    max_history: int

    @classmethod
    def from_env(cls):
        load_dotenv()
        raw_path = os.getenv("CALC_HISTORY_FILE", "calculator_history.csv")
        if not raw_path.strip():
            raise ConfigurationError("CALC_HISTORY_FILE cannot be blank.")
        raw_auto = os.getenv("CALC_AUTO_SAVE", "true").strip().lower()
        if raw_auto not in {"true", "false"}:
            raise ConfigurationError("CALC_AUTO_SAVE must be true or false.")
        try:
            limit = int(os.getenv("CALC_MAX_HISTORY", "1000"))
        except ValueError as exc:
            raise ConfigurationError("CALC_MAX_HISTORY must be a positive integer.") from exc
        if limit <= 0:
            raise ConfigurationError("CALC_MAX_HISTORY must be positive.")
        return cls(Path(raw_path).expanduser(), raw_auto == "true", limit)
