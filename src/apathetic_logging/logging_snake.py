# src/apathetic_logging/logging_snake.py
"""Snake case convenience functions for standard logging module."""

from __future__ import annotations


class ApatheticLogging_Internal_LoggingSnakeCase:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides snake_case convenience functions for logging.*.

    This class contains snake_case wrapper functions for standard library
    `logging.*` functions that use camelCase naming. These wrappers provide
    a more Pythonic interface that follows PEP 8 naming conventions while
    maintaining full compatibility with the underlying logging module functions.

    When mixed into apathetic_logging, it provides snake_case alternatives
    to standard logging module functions (e.g., `basicConfig` -> `basic_config`,
    `addLevelName` -> `add_level_name`, `setLoggerClass` -> `set_logger_class`).
    """
