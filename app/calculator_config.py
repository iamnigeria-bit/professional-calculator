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

    log_dir: Path = Path("logs")
    history_dir: Path = Path(".")
    precision: int = 2
    max_input_value: float = 1_000_000_000.0
    default_encoding: str = "utf-8"

    @classmethod
    def from_env(cls):
        load_dotenv()

        raw_path = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            os.getenv("CALC_HISTORY_FILE", "calculator_history.csv"),
        )
        if not raw_path.strip():
            raise ConfigurationError("CALC_HISTORY_FILE cannot be blank.")

        raw_auto = os.getenv(
            "CALCULATOR_AUTO_SAVE",
            os.getenv("CALC_AUTO_SAVE", "true"),
        ).strip().lower()
        if raw_auto not in {"true", "false"}:
            raise ConfigurationError("CALC_AUTO_SAVE must be true or false.")

        try:
            limit = int(
                os.getenv(
                    "CALCULATOR_MAX_HISTORY_SIZE",
                    os.getenv("CALC_MAX_HISTORY", "1000"),
                )
            )
        except ValueError as exc:
            raise ConfigurationError(
                "CALC_MAX_HISTORY must be a positive integer."
            ) from exc

        if limit <= 0:
            raise ConfigurationError("CALC_MAX_HISTORY must be positive.")

        return cls(
            history_file=Path(raw_path).expanduser(),
            auto_save=raw_auto == "true",
            max_history=limit,
            log_dir=Path(
                os.getenv("CALCULATOR_LOG_DIR", "logs")
            ).expanduser(),
            history_dir=Path(
                os.getenv("CALCULATOR_HISTORY_DIR", ".")
            ).expanduser(),
            precision=int(
                os.getenv("CALCULATOR_PRECISION", "2")
            ),
            max_input_value=float(
                os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000000")
            ),
            default_encoding=os.getenv(
                "CALCULATOR_DEFAULT_ENCODING", "utf-8"
            ),
        )