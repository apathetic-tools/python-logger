# tests/95_app_integration/test_custom_logger_basic.py
"""Tests for correct custom logger usage patterns from docs/custom-logger.md."""

import argparse
import logging
from typing import cast

# Import from conftest in same directory
import conftest
import pytest

import apathetic_logging as mod_alogs


AppLoggerForTest = conftest.AppLoggerForTest
AppLoggerWithCustomMethodForTest = conftest.AppLoggerWithCustomMethodForTest


def test_custom_logger_correct_usage_pattern() -> None:
    """Test the correct usage pattern from docs/custom-logger.md."""
    # --- setup ---
    app_name = "testapp"
    default_log_level = "info"
    log_level_env_var = "TESTAPP_LOG_LEVEL"

    # Step 1: Extend the logging module (must happen first)
    # Note: This sets the logger class globally, so logging.getLogger()
    # will create instances of AppLoggerForTest
    AppLoggerForTest.extend_logging_module()

    # Step 2: Register environment variables
    mod_alogs.register_log_level_env_vars([log_level_env_var, "LOG_LEVEL"])

    # Step 3: Register default log level
    mod_alogs.register_default_log_level(default_log_level)

    # Step 4: Register logger name
    mod_alogs.register_logger_name(app_name)

    # Step 5: Get logger instance
    # Since extend_logging_module() was called, this will be AppLoggerForTest
    logger = cast("AppLoggerForTest", logging.getLogger(app_name))

    # --- verify ---
    assert logger is not None
    assert logger.name == app_name
    assert isinstance(logger, mod_alogs.Logger)
    # Should be able to use custom levels
    logger.setLevel("TRACE")
    assert logger.level_name == "TRACE"
    logger.setLevel("SILENT")
    assert logger.level_name == "SILENT"


def test_custom_logger_with_typed_getter() -> None:
    """Test custom logger with typed getter function."""
    # --- setup ---
    app_name = "testapp_typed"
    AppLoggerForTest.extend_logging_module()
    mod_alogs.register_logger_name(app_name)

    def get_app_logger() -> AppLoggerForTest:
        """Return the configured application logger."""
        logger = cast("AppLoggerForTest", mod_alogs.get_logger())
        return logger

    # --- execute ---
    logger = get_app_logger()

    # --- verify ---
    assert logger is not None
    assert logger.name == app_name
    # Check that logger has expected apathetic_logging.Logger methods/behavior
    # (instead of isinstance check which may fail in singlefile mode due to class
    # reference differences)
    assert hasattr(logger, "trace")
    assert hasattr(logger, "colorize")
    assert hasattr(logger, "determine_log_level")


def test_custom_logger_determine_log_level_with_cli_args(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that CLI args override environment variables and root log level."""
    # --- setup ---
    app_name = "testapp_determine_cli"
    AppLoggerForTest.extend_logging_module()
    mod_alogs.register_logger_name(app_name)
    logger = AppLoggerForTest(app_name)

    # Set up conflicting values that CLI args should override
    monkeypatch.setenv("TESTAPP_LOG_LEVEL", "info")
    root_log_level = "info"

    # --- execute ---
    args = argparse.Namespace(log_level="debug")
    level = logger.determine_log_level(args=args, root_log_level=root_log_level)

    # --- verify ---
    # CLI args should override both env var and root log level
    assert level == "DEBUG"


def test_custom_logger_determine_log_level_with_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that environment variables override root log level."""
    # --- setup ---
    app_name = "testapp_determine_env"
    AppLoggerForTest.extend_logging_module()
    mod_alogs.register_logger_name(app_name)
    logger = AppLoggerForTest(app_name)

    # Set up conflicting root log level that env var should override
    root_log_level = "info"

    # --- execute ---
    monkeypatch.setenv("TESTAPP_LOG_LEVEL", "warning")
    level = logger.determine_log_level(root_log_level=root_log_level)

    # --- verify ---
    # Env var should override root log level
    assert level == "WARNING"


def test_custom_logger_determine_log_level_with_root_log_level(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that root log level is used when no CLI args or env vars are set."""
    # --- setup ---
    app_name = "testapp_determine_root"
    AppLoggerForTest.extend_logging_module()
    mod_alogs.register_logger_name(app_name)
    logger = AppLoggerForTest(app_name)

    # Ensure no env vars are set
    monkeypatch.delenv("TESTAPP_LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    # --- execute ---
    level = logger.determine_log_level(root_log_level="error")

    # --- verify ---
    # Root log level should be used when nothing else is set
    assert level == "ERROR"


def test_custom_logger_determine_log_level_default_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that determine_log_level() falls back to default when nothing is set."""
    # --- setup ---
    app_name = "testapp_determine_default"
    AppLoggerForTest.extend_logging_module()
    mod_alogs.register_logger_name(app_name)
    logger = AppLoggerForTest(app_name)

    # Ensure no env vars or other settings are set
    monkeypatch.delenv("TESTAPP_LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    # --- execute ---
    # No CLI args, no env vars, no root log level - should use default
    level = logger.determine_log_level()

    # --- verify ---
    # Should fall back to default (INFO)
    assert level == "INFO"


def test_custom_logger_with_custom_methods() -> None:
    """Test custom logger with application-specific methods."""
    # --- setup ---
    app_name = "testapp_custom_methods"
    # Need to set logger class to our custom class
    AppLoggerWithCustomMethodForTest.extend_logging_module()
    mod_alogs.register_logger_name(app_name)
    # Create logger directly to ensure we get the right type
    logger = AppLoggerWithCustomMethodForTest(app_name)

    # --- verify ---
    assert hasattr(logger, "log_operation")
    assert hasattr(logger, "log_performance")
    assert callable(logger.log_operation)
    assert callable(logger.log_performance)

    # Test custom methods work
    logger.setLevel("INFO")
    logger.log_operation("test_op", "success")
    logger.setLevel("DEBUG")
    logger.log_performance("latency", 42.5)
