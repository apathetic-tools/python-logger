# src/serger/utils/utils_logs.py
"""Shared Apathetic CLI logger implementation."""

from __future__ import annotations

import inspect
import logging
from typing import cast

from .constants import _ApatheticLogger_Constants  # pyright: ignore[reportPrivateUsage]
from .dual_stream_handler import (
    _ApatheticLogger_DualStreamHandler,  # pyright: ignore[reportPrivateUsage]
)
from .logger import _ApatheticLogger_Logger  # pyright: ignore[reportPrivateUsage]
from .register_default_log_level import (
    _ApatheticLogger_RegisterDefaultLogLevel,  # pyright: ignore[reportPrivateUsage]
)
from .register_log_level_env_vars import (
    _ApatheticLogger_RegisterLogLevelEnvVars,  # pyright: ignore[reportPrivateUsage]
)
from .register_logger_name import (
    _ApatheticLogger_RegisterLoggerName,  # pyright: ignore[reportPrivateUsage]
)
from .safe_log import _ApatheticLogger_SafeLog  # pyright: ignore[reportPrivateUsage]
from .tag_formatter import (
    _ApatheticLogger_TagFormatter,  # pyright: ignore[reportPrivateUsage]
)
from .test_trace import (
    _ApatheticLogger_TestTrace,  # pyright: ignore[reportPrivateUsage]
)


# --- globals ---------------------------------------------------------------

# Registry for configurable log level settings
# These must be module-level for global state management
_registered_log_level_env_vars: list[str] | None = None
_registered_default_log_level: str | None = None
_registered_logger_name: str | None = None


# --- Apathetic Logger Namespace -------------------------------------------


class ApatheticLogger(  # pyright: ignore[reportPrivateUsage]
    _ApatheticLogger_Constants,
    _ApatheticLogger_DualStreamHandler,
    _ApatheticLogger_Logger,
    _ApatheticLogger_RegisterDefaultLogLevel,
    _ApatheticLogger_RegisterLogLevelEnvVars,
    _ApatheticLogger_RegisterLoggerName,
    _ApatheticLogger_SafeLog,
    _ApatheticLogger_TagFormatter,
    _ApatheticLogger_TestTrace,
):
    """Namespace for apathetic logger functionality.

    All logger functionality is accessed via this namespace class to minimize
    global namespace pollution when the library is embedded in a stitched script.

    The Logger class is provided via the _ApatheticLogger_Logger mixin.
    The TagFormatter class is provided via the _ApatheticLogger_TagFormatter mixin.
    The DualStreamHandler class is provided via the
    _ApatheticLogger_DualStreamHandler mixin.
    The register_default_log_level static method is provided via the
    _ApatheticLogger_RegisterDefaultLogLevel mixin.
    The register_log_level_env_vars static method is provided via the
    _ApatheticLogger_RegisterLogLevelEnvVars mixin.
    The register_logger_name static method is provided via the
    _ApatheticLogger_RegisterLoggerName mixin.
    The safe_log static method is provided via the _ApatheticLogger_SafeLog mixin.
    The TEST_TRACE and make_test_trace static methods are provided via the
    _ApatheticLogger_TestTrace mixin.
    """

    # --- Static Methods ----------------------------------------------------

    @staticmethod
    def get_logger() -> ApatheticLogger.Logger:
        """Return the registered logger instance.

        Uses Python's built-in logging registry (logging.getLogger()) to retrieve
        the logger. If no logger name has been registered, attempts to auto-infer
        the logger name from the calling module's top-level package.

        Returns:
            The logger instance from logging.getLogger()
            (as ApatheticLogger.Logger type)

        Raises:
            RuntimeError: If called before a logger name has been registered and
                auto-inference fails.

        Note:
            This function is used internally by utils_logs.py. Applications
            should use their app-specific getter (e.g., get_app_logger()) for
            better type hints.
        """
        global _registered_logger_name  # noqa: PLW0603

        if _registered_logger_name is None:
            # Try to auto-infer from the calling module's package
            frame = inspect.currentframe()
            if frame is not None:
                try:
                    # Get the calling frame (skip get_logger itself)
                    caller_frame = frame.f_back
                    if caller_frame is not None:
                        caller_module = caller_frame.f_globals.get("__package__")
                        if caller_module:
                            inferred_name = ApatheticLogger._extract_top_level_package(
                                caller_module
                            )
                            if inferred_name:
                                _registered_logger_name = inferred_name
                                ApatheticLogger.TEST_TRACE(
                                    "get_logger() auto-inferred logger name",
                                    f"name={inferred_name}",
                                    f"from_module={caller_module}",
                                )
                finally:
                    del frame

        if _registered_logger_name is None:
            _msg = (
                "Logger name not registered and could not be auto-inferred. "
                "Call register_logger_name() or ensure your app's logs "
                "module is imported."
            )
            raise RuntimeError(_msg)

        logger = logging.getLogger(_registered_logger_name)
        typed_logger = cast("ApatheticLogger.Logger", logger)
        ApatheticLogger.TEST_TRACE(
            "get_logger() called",
            f"name={typed_logger.name}",
            f"id={id(typed_logger)}",
            f"level={typed_logger.level_name}",
            f"handlers={[type(h).__name__ for h in typed_logger.handlers]}",
        )
        return typed_logger


# --- Module-level validation -----------------------------------------------

# sanity check
if __debug__:
    _tag_levels = set(ApatheticLogger.TAG_STYLES.keys())
    _known_levels = {lvl.upper() for lvl in ApatheticLogger.LEVEL_ORDER}
    if not _tag_levels <= _known_levels:
        _msg = "TAG_STYLES contains unknown levels"
        raise AssertionError(_msg)
