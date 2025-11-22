# tests/70_snake/test_module_lib_snake.py
"""Test module-level library snake_case convenience functions."""

from __future__ import annotations

import importlib
from contextlib import suppress
from unittest.mock import MagicMock

import pytest

import apathetic_logging as mod_alogs
from tests.utils.patch_everywhere import patch_everywhere


# List of all library module-level snake_case functions and their test parameters
# Format: (function_name, args, kwargs, mock_target_module, mock_target_function)
MODULE_LIB_SNAKE_TESTS: list[
    tuple[str, tuple[object, ...], dict[str, object], str, str]
] = [
    ("get_logger", (None,), {}, "apathetic_logging.get_logger", "getLogger"),
    (
        "get_logger_of_type",
        ("test", object),
        {},
        "apathetic_logging.get_logger",
        "getLoggerOfType",
    ),
    ("has_logger", ("test",), {}, "apathetic_logging.logging_utils", "hasLogger"),
    (
        "remove_logger",
        ("test",),
        {},
        "apathetic_logging.logging_utils",
        "removeLogger",
    ),
    (
        "register_default_log_level",
        ("INFO",),
        {},
        "apathetic_logging.registry",
        "registerDefaultLogLevel",
    ),
    (
        "register_log_level_env_vars",
        (["LOG_LEVEL"],),
        {},
        "apathetic_logging.registry",
        "registerLogLevelEnvVars",
    ),
    (
        "register_logger",
        ("test",),
        {},
        "apathetic_logging.registry",
        "registerLogger",
    ),
    (
        "get_default_logger_name",
        ("test",),
        {},
        "apathetic_logging.logging_utils",
        "getDefaultLoggerName",
    ),
    (
        "get_log_level_env_vars",
        (),
        {},
        "apathetic_logging.registry",
        "getLogLevelEnvVars",
    ),
    (
        "get_default_log_level",
        (),
        {},
        "apathetic_logging.registry",
        "getDefaultLogLevel",
    ),
    (
        "get_registered_logger_name",
        (),
        {},
        "apathetic_logging.registry",
        "getRegisteredLoggerName",
    ),
    (
        "get_target_python_version",
        (),
        {},
        "apathetic_logging.registry",
        "getTargetPythonVersion",
    ),
    (
        "get_default_propagate",
        (),
        {},
        "apathetic_logging.registry",
        "getDefaultPropagate",
    ),
    ("safe_log", ("test",), {}, "apathetic_logging.safe_logging", "safeLog"),
    (
        "safe_trace",
        ("test",),
        {},
        "apathetic_logging.safe_logging",
        "safeTrace",
    ),
    (
        "make_safe_trace",
        ("test",),
        {},
        "apathetic_logging.safe_logging",
        "makeSafeTrace",
    ),
]


@pytest.mark.parametrize(
    ("func_name", "args", "kwargs", "mock_target_module", "mock_target_function"),
    MODULE_LIB_SNAKE_TESTS,
)
def test_module_lib_snake_function(
    func_name: str,
    args: tuple[object, ...],
    kwargs: dict[str, object],
    mock_target_module: str,
    mock_target_function: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test module-level library snake_case functions call camelCase function.

    This is a "happy path" test that verifies each snake_case wrapper function
    exists and calls the underlying library function correctly.
    """
    # Get the snake_case function
    snake_func = getattr(mod_alogs, func_name)
    assert snake_func is not None, (
        f"Function {func_name} not found on apathetic_logging"
    )

    # Mock the underlying library function
    # For library functions, patch the internal class method that the snake_case
    # function calls. Use patch_everywhere to patch the class method everywhere
    # it was imported (handles both package and stitched single-file runtimes).
    if mock_target_module.startswith("apathetic_logging."):
        # Import the module and get the class
        mod = importlib.import_module(mock_target_module)
        if mock_target_module == "apathetic_logging.get_logger":
            target_class = mod.ApatheticLogging_Internal_GetLogger
        elif mock_target_module == "apathetic_logging.logging_utils":
            target_class = mod.ApatheticLogging_Internal_LoggingUtils
        elif mock_target_module == "apathetic_logging.registry":
            target_class = mod.ApatheticLogging_Internal_Registry
        elif mock_target_module == "apathetic_logging.safe_logging":
            target_class = mod.ApatheticLogging_Internal_SafeLogging
        else:
            # Fallback: try namespace class
            target_class = getattr(mod, "apathetic_logging", None)
            if target_class is None:
                pytest.skip(f"Could not find target class in {mock_target_module}")

        mock_func = MagicMock()
        patch_everywhere(
            monkeypatch,
            target_class,
            mock_target_function,
            mock_func,
        )
        # Call the snake_case function
        # Some functions may raise (e.g., if logger doesn't exist)
        # That's okay - we just want to verify the mock was called
        with suppress(Exception):
            snake_func(*args, **kwargs)

        # Verify the underlying function was called
        assert mock_func.called, f"{mock_target_function} was not called by {func_name}"
    else:
        # For stdlib functions, use standard patch (not in our package)
        pytest.skip(f"Stdlib functions not supported: {mock_target_module}")


def test_module_lib_snake_function_exists() -> None:
    """Verify all expected snake_case functions exist on apathetic_logging."""
    for func_name, _, _, _, _ in MODULE_LIB_SNAKE_TESTS:
        assert hasattr(mod_alogs, func_name), (
            f"Function {func_name} should exist on apathetic_logging"
        )
