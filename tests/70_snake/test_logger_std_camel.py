# tests/70_snake/test_logger_std_camel.py
"""Test module-level stdlib camelCase convenience functions."""

from __future__ import annotations

import logging
import sys
from contextlib import suppress
from unittest.mock import patch

import pytest

import apathetic_logging as mod_alogs
from tests.utils.level_validation import validate_test_level


# Safe test level value (26 is between MINIMAL=25 and WARNING=30)
TEST_LEVEL_VALUE = 26
validate_test_level(TEST_LEVEL_VALUE)

# List of all stdlib module-level camelCase functions and their test parameters
# Format: (function_name, args, kwargs, mock_target)
MODULE_STD_CAMEL_TESTS: list[tuple[str, tuple[object, ...], dict[str, object], str]] = [
    ("basicConfig", (), {}, "logging.basicConfig"),
    (
        "addLevelName",
        (TEST_LEVEL_VALUE, "CUSTOM_TEST_LEVEL"),
        {},
        "logging.addLevelName",
    ),
    ("getLevelName", (logging.DEBUG,), {}, "logging.getLevelName"),
    ("getLevelNamesMapping", (), {}, "logging.getLevelNamesMapping"),
    ("getLoggerClass", (), {}, "logging.getLoggerClass"),
    ("setLoggerClass", (object,), {}, "logging.setLoggerClass"),
    ("getLogRecordFactory", (), {}, "logging.getLogRecordFactory"),
    ("setLogRecordFactory", (object,), {}, "logging.setLogRecordFactory"),
    ("shutdown", (), {}, "logging.shutdown"),
    ("disable", (logging.DEBUG,), {}, "logging.disable"),
    ("captureWarnings", (True,), {}, "logging.captureWarnings"),
    ("critical", ("test",), {}, "logging.critical"),
    ("debug", ("test",), {}, "logging.debug"),
    ("error", ("test",), {}, "logging.error"),
    ("exception", ("test",), {"exc_info": True}, "logging.exception"),
    ("fatal", ("test",), {}, "logging.fatal"),
    ("info", ("test",), {}, "logging.info"),
    ("log", (logging.INFO, "test"), {}, "logging.log"),
    ("warn", ("test",), {}, "logging.warning"),
    ("warning", ("test",), {}, "logging.warning"),
    ("getLogger", ("test",), {}, "logging.getLogger"),
    ("makeLogRecord", ({"name": "test"},), {}, "logging.makeLogRecord"),
    ("currentframe", (), {}, "logging.currentframe"),
    ("getHandlerNames", (), {}, "logging.getHandlerNames"),
    ("getHandlerByName", ("test",), {}, "logging.getHandlerByName"),
]


@pytest.mark.parametrize(
    ("func_name", "args", "kwargs", "mock_target"),
    MODULE_STD_CAMEL_TESTS,
)
def test_module_std_camel_function(
    func_name: str,
    args: tuple[object, ...],
    kwargs: dict[str, object],
    mock_target: str,
) -> None:
    """Test module-level stdlib camelCase functions call camelCase function.

    This is a "happy path" test that verifies each camelCase wrapper function
    exists and calls the underlying stdlib function correctly.
    """
    # Get the camelCase function
    camel_func = getattr(mod_alogs, func_name)
    assert camel_func is not None, (
        f"Function {func_name} not found on apathetic_logging"
    )

    # Check if the underlying function exists before trying to patch it
    # Some functions don't exist in Python 3.10
    # (e.g., getLevelNamesMapping, getHandlerNames, getHandlerByName)
    module_name, func_name_in_module = mock_target.rsplit(".", 1)
    if module_name == "logging" and not hasattr(logging, func_name_in_module):
        py_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
        pytest.skip(
            f"{func_name} requires {func_name_in_module} which doesn't exist "
            f"in logging module on Python {py_version}"
        )

    # Mock the underlying stdlib function
    with patch(mock_target) as mock_func:
        # Call the camelCase function
        # Some functions may raise (e.g., if logging is already configured)
        # That's okay - we just want to verify the mock was called
        with suppress(Exception):
            camel_func(*args, **kwargs)

        # Verify the underlying function was called
        mock_func.assert_called_once_with(*args, **kwargs)


def test_module_std_camel_function_exists() -> None:
    """Verify all expected camelCase functions exist on apathetic_logging."""
    for func_name, _, _, _ in MODULE_STD_CAMEL_TESTS:
        assert hasattr(mod_alogs, func_name), (
            f"Function {func_name} should exist on apathetic_logging"
        )
