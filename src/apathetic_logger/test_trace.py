"""TestTrace functionality for Apathetic Logger."""

from __future__ import annotations

import builtins
import importlib
import sys
from collections.abc import Callable
from typing import Any


# Lazy, safe import — avoids patched time modules
#   in environments like pytest or eventlet
_real_time = importlib.import_module("time")


def _get_namespace_module() -> Any:
    """Get the namespace module at runtime.

    This avoids circular import issues by accessing the namespace
    through the module system after it's been created.
    """
    # Access through sys.modules to avoid circular import
    namespace_module = sys.modules.get("apathetic_logger.namespace")
    if namespace_module is None:
        # Fallback: import if not yet loaded
        namespace_module = sys.modules["apathetic_logger.namespace"]
    return namespace_module


def _get_namespace() -> Any:
    """Get the ApatheticLogger namespace at runtime."""
    return _get_namespace_module().ApatheticLogger


class _ApatheticLogger_TestTrace:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides the TEST_TRACE and make_test_trace static methods.

    This class contains the TEST_TRACE implementation as static methods.
    When mixed into ApatheticLogger, it provides ApatheticLogger.TEST_TRACE
    and ApatheticLogger.make_test_trace.
    """

    @staticmethod
    def make_test_trace(icon: str = "🧪") -> Callable[..., Any]:
        def local_trace(label: str, *args: Any) -> Any:
            ns = _get_namespace()
            return ns.TEST_TRACE(label, *args, icon=icon)

        return local_trace

    @staticmethod
    def TEST_TRACE(label: str, *args: Any, icon: str = "🧪") -> None:  # noqa: N802
        """Emit a synchronized, flush-safe diagnostic line.

        Args:
            label: Short identifier or context string.
            *args: Optional values to append.
            icon: Emoji prefix/suffix for easier visual scanning.

        """
        ns = _get_namespace()
        if not ns.TEST_TRACE_ENABLED:
            return

        ts = _real_time.monotonic()
        # builtins.print more reliable than sys.stdout.write + sys.stdout.flush
        builtins.print(
            f"{icon} [TEST TRACE {ts:.6f}] {label}",
            *args,
            file=sys.__stderr__,
            flush=True,
        )
