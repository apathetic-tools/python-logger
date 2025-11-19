# src/apathetic_logging/safe_logging.py
"""Safe logging utilities for Apathetic Logging."""

from __future__ import annotations

import builtins
import importlib
import sys
from collections.abc import Callable
from contextlib import suppress
from typing import Any, TextIO, cast

from .constants import (
    ApatheticLogging_Internal_Constants,
)


# Lazy, safe import — avoids patched time modules
#   in environments like pytest or eventlet
_real_time = importlib.import_module("time")


class ApatheticLogging_Internal_SafeLogging:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides safe logging utilities.

    This class contains both safe_log and safe_trace implementations as static
    methods. When mixed into apathetic_logging, it provides:
    - apathetic_logging.safe_log
    - apathetic_logging.safe_trace
    - apathetic_logging.make_safe_trace
    """

    @staticmethod
    def safe_log(msg: str) -> None:
        """Emergency logger that never fails."""
        stream = cast("TextIO", sys.__stderr__)
        try:
            print(msg, file=stream)
        except Exception:  # noqa: BLE001
            # As final guardrail — never crash during crash reporting
            with suppress(Exception):
                stream.write(f"[INTERNAL] {msg}\n")

    @staticmethod
    def make_safe_trace(icon: str = "🧪") -> Callable[..., Any]:
        _safe_logging = ApatheticLogging_Internal_SafeLogging

        def local_trace(label: str, *args: Any) -> Any:
            return _safe_logging.safe_trace(label, *args, icon=icon)

        return local_trace

    @staticmethod
    def safe_trace(label: str, *args: Any, icon: str = "🧪") -> None:
        """Emit a synchronized, flush-safe diagnostic line.

        Args:
            label: Short identifier or context string.
            *args: Optional values to append.
            icon: Emoji prefix/suffix for easier visual scanning.

        """
        _constants = ApatheticLogging_Internal_Constants
        if not _constants.SAFE_TRACE_ENABLED:
            return

        ts = _real_time.monotonic()
        # builtins.print more reliable than sys.stdout.write + sys.stdout.flush
        builtins.print(
            f"{icon} [SAFE TRACE {ts:.6f}] {label}",
            *args,
            file=sys.__stderr__,
            flush=True,
        )
