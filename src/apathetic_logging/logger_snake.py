# src/apathetic_logging/logger_snake.py
"""Snake case convenience functions for logging.Logger."""

from __future__ import annotations


class ApatheticLogging_Internal_LoggerSnakeCase:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides snake_case convenience methods for logging.Logger.

    This class contains snake_case wrapper methods for standard library
    `logging.Logger` methods that use camelCase naming. These wrappers provide
    a more Pythonic interface that follows PEP 8 naming conventions while
    maintaining full compatibility with the underlying logging.Logger methods.

    When mixed into Logger, it provides snake_case alternatives to standard
    Logger methods (e.g., `addHandler` -> `add_handler`, `removeHandler` ->
    `remove_handler`, `setLevel` -> `set_level`, `getEffectiveLevel` ->
    `get_effective_level`).
    """
