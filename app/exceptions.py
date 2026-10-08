"""Domain-specific calculator exceptions."""

class CalculatorError(ValueError):
    """Base error for user-facing calculator failures."""

class OperationError(CalculatorError):
    """Invalid or unsupported arithmetic operation."""

class ConfigurationError(CalculatorError):
    """Invalid application settings."""
