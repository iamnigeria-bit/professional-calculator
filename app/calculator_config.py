
"""Validated environment-based calculator configuration."""

import codecs
import math
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

    log_dir: Path = Path("logs")
    history_dir: Path = Path(".")
    precision: int = 2
    max_input_value: float = 1_000_000_000.0
    default_encoding: str = "utf-8"

    @classmethod
    def from_env(cls):
        """Load and validate configuration settings."""
        load_dotenv()

        raw_path = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            os.getenv("CALC_HISTORY_FILE", "calculator_history.csv")
        )

        if not raw_path.strip():
            raise ConfigurationError(
                "CALCULATOR_HISTORY_FILE cannot be blank."
            )

        raw_auto = os.getenv(
            "CALCULATOR_AUTO_SAVE",
            os.getenv("CALC_AUTO_SAVE", "true")
        ).strip().lower()

        if raw_auto not in {"true", "false"}:
            raise ConfigurationError(
                "CALCULATOR_AUTO_SAVE must be true or false."
            )

        try:
            max_history = int(
                os.getenv(
                    "CALCULATOR_MAX_HISTORY_SIZE",
                    os.getenv("CALC_MAX_HISTORY", "1000")
                )
            )
        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be an integer."
            ) from exc

        if max_history <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be positive."
            )

        try:
            precision = int(
                os.getenv("CALCULATOR_PRECISION", "2")
            )
        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_PRECISION must be an integer."
            ) from exc

        if not 0 <= precision <= 15:
            raise ConfigurationError(
                "CALCULATOR_PRECISION must be between 0 and 15."
            )

        try:
            max_input = float(
                os.getenv(
                    "CALCULATOR_MAX_INPUT_VALUE",
                    "1000000000"
                )
            )
        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be numeric."
            ) from exc

        if not math.isfinite(max_input) or max_input <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be finite and positive."
            )

        encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        ).strip()

        if not encoding:
            raise ConfigurationError(
                "CALCULATOR_DEFAULT_ENCODING cannot be blank."
            )

        try:
            codecs.lookup(encoding)
        except LookupError as exc:
            raise ConfigurationError(
                f"Unsupported file encoding: {encoding}"
            ) from exc

        log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        history_dir = os.getenv("CALCULATOR_HISTORY_DIR", ".")

        if not log_dir.strip() or not history_dir.strip():
            raise ConfigurationError(
                "Log and history directories cannot be blank."
            )

        return cls(
            history_file=Path(raw_path).expanduser(),
            auto_save=raw_auto == "true",
            max_history=max_history,
            log_dir=Path(log_dir).expanduser(),
            history_dir=Path(history_dir).expanduser(),
            precision=precision,
            max_input_value=max_input,
            default_encoding=encoding
        )
