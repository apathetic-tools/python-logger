# src/apathetic_logging/__init__.py
"""Apathetic Logging implementation."""

# Get reference to the namespace class
# In stitched mode: class is already defined in namespace.py (executed before this)
# In installed mode: import from namespace module and initialize
_is_standalone = globals().get("__STANDALONE__", False)

if _is_standalone:
    # Stitched mode: class already defined in namespace.py
    # Get reference to the class (it's already in globals from namespace.py)
    _apathetic_logging_ns = globals().get("apathetic_logging")
    if _apathetic_logging_ns is None:
        # Fallback: should not happen, but handle gracefully
        msg = "apathetic_logging class not found in standalone mode"
        raise RuntimeError(msg)
else:
    from .namespace import apathetic_logging as _apathetic_logging_ns

    # Export the namespace class itself (only if not already defined)
    if "apathetic_logging" not in globals():
        apathetic_logging = _apathetic_logging_ns

# Export all namespace items for convenience
# These are aliases to apathetic_logging.*
#
# Note: In embedded builds, __init__.py is excluded from the stitch,
# so this code never runs and no exports happen (only the class is available).
# In singlefile/installed builds, __init__.py is included, so exports happen.
DEFAULT_APATHETIC_LOG_LEVEL = _apathetic_logging_ns.DEFAULT_APATHETIC_LOG_LEVEL
DEFAULT_APATHETIC_LOG_LEVEL_ENV_VARS = (
    _apathetic_logging_ns.DEFAULT_APATHETIC_LOG_LEVEL_ENV_VARS
)
LEVEL_ORDER = _apathetic_logging_ns.LEVEL_ORDER
SILENT_LEVEL = _apathetic_logging_ns.SILENT_LEVEL
TAG_STYLES = _apathetic_logging_ns.TAG_STYLES
TEST_TRACE = _apathetic_logging_ns.TEST_TRACE
TEST_TRACE_ENABLED = _apathetic_logging_ns.TEST_TRACE_ENABLED
TRACE_LEVEL = _apathetic_logging_ns.TRACE_LEVEL

# ANSI Colors
ANSIColors = _apathetic_logging_ns.ANSIColors

# Classes
DualStreamHandler = _apathetic_logging_ns.DualStreamHandler
TagFormatter = _apathetic_logging_ns.TagFormatter

# Functions
get_logger = _apathetic_logging_ns.get_logger
make_test_trace = _apathetic_logging_ns.make_test_trace
register_default_log_level = _apathetic_logging_ns.register_default_log_level
register_log_level_env_vars = _apathetic_logging_ns.register_log_level_env_vars
register_logger_name = _apathetic_logging_ns.register_logger_name
safe_log = _apathetic_logging_ns.safe_log


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
    "DualStreamHandler",
    "TagFormatter",
    "apathetic_logging",
    "get_logger",
    "make_test_trace",
    "register_default_log_level",
    "register_log_level_env_vars",
    "register_logger_name",
    "safe_log",
]
