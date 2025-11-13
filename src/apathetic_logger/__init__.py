"""Apathetic Logger implementation."""

from .logger import ApatheticLogger as _ApatheticLoggerNamespace


# Ensure logging module is extended with TRACE and SILENT levels
# This must be called before any loggers are created
_ApatheticLoggerNamespace.Logger.extend_logging_module()


# Export the namespace class
# In stitched version, only this will be in global namespace
ApatheticLogger = _ApatheticLoggerNamespace

# Export all namespace items for convenience
# These are aliases to ApatheticLogger.*
DEFAULT_APATHETIC_LOG_LEVEL = _ApatheticLoggerNamespace.DEFAULT_APATHETIC_LOG_LEVEL
DEFAULT_APATHETIC_LOG_LEVEL_ENV_VARS = (
    _ApatheticLoggerNamespace.DEFAULT_APATHETIC_LOG_LEVEL_ENV_VARS
)
LEVEL_ORDER = _ApatheticLoggerNamespace.LEVEL_ORDER
SILENT_LEVEL = _ApatheticLoggerNamespace.SILENT_LEVEL
TAG_STYLES = _ApatheticLoggerNamespace.TAG_STYLES
TEST_TRACE = _ApatheticLoggerNamespace.TEST_TRACE
TEST_TRACE_ENABLED = _ApatheticLoggerNamespace.TEST_TRACE_ENABLED
TRACE_LEVEL = _ApatheticLoggerNamespace.TRACE_LEVEL

# ANSI Colors
ANSIColors = _ApatheticLoggerNamespace.ANSIColors

# Classes
DualStreamHandler = _ApatheticLoggerNamespace.DualStreamHandler
TagFormatter = _ApatheticLoggerNamespace.TagFormatter

# Functions
get_logger = _ApatheticLoggerNamespace.get_logger
make_test_trace = _ApatheticLoggerNamespace.make_test_trace
register_default_log_level = _ApatheticLoggerNamespace.register_default_log_level
register_log_level_env_vars = _ApatheticLoggerNamespace.register_log_level_env_vars
register_logger_name = _ApatheticLoggerNamespace.register_logger_name
safe_log = _ApatheticLoggerNamespace.safe_log


__all__ = [
    "DEFAULT_APATHETIC_LOG_LEVEL",
    "DEFAULT_APATHETIC_LOG_LEVEL_ENV_VARS",
    "LEVEL_ORDER",
    "SILENT_LEVEL",
    "TAG_STYLES",
    "TEST_TRACE",
    "TEST_TRACE_ENABLED",
    "TRACE_LEVEL",
    "ANSIColors",
    "ApatheticLogger",
    "DualStreamHandler",
    "TagFormatter",
    "get_logger",
    "make_test_trace",
    "register_default_log_level",
    "register_log_level_env_vars",
    "register_logger_name",
    "safe_log",
]
