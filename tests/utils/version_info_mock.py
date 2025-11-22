# tests/utils/version_info_mock.py
# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportAttributeAccessIssue=false

"""Utilities for creating mock sys.version_info objects in tests."""

from collections.abc import Callable
from types import SimpleNamespace
from typing import Any


def create_version_info(major: int, minor: int, micro: int = 0) -> Any:
    """Create a mock sys.version_info object with major and minor attributes.

    This properly mocks sys.version_info so it can be used with attribute access
    (.major, .minor) and tuple comparison, matching the behavior of the real
    sys.version_info object.

    Args:
        major: Major version number (e.g., 3)
        minor: Minor version number (e.g., 11)
        micro: Micro version number (default: 0)

    Returns:
        A mock version_info object with .major, .minor, .micro attributes
        and tuple-like comparison support.
    """
    version_info = SimpleNamespace()
    version_info.major = major
    version_info.minor = minor
    version_info.micro = micro

    # Make it comparable with tuples and other version_info objects
    def _get_tuple(obj: Any) -> tuple[int, int] | None:
        """Extract (major, minor) tuple from version_info or tuple."""
        if isinstance(obj, tuple) and len(obj) >= 2:  # noqa: PLR2004
            return (int(obj[0]), int(obj[1]))
        if hasattr(obj, "major") and hasattr(obj, "minor"):
            return (int(obj.major), int(obj.minor))
        return None

    def _compare(self: Any, other: Any, op: str) -> Any:
        """Compare version_info with tuples or other version_info objects."""
        self_tuple = (self.major, self.minor)
        other_tuple = _get_tuple(other)
        if other_tuple is None:
            return NotImplemented

        ops: dict[str, Callable[[], bool]] = {
            "<": lambda: self_tuple < other_tuple,
            "<=": lambda: self_tuple <= other_tuple,
            ">": lambda: self_tuple > other_tuple,
            ">=": lambda: self_tuple >= other_tuple,
            "==": lambda: self_tuple == other_tuple,
            "!=": lambda: self_tuple != other_tuple,
        }
        if op in ops:
            return ops[op]()
        return NotImplemented

    def make_comparator(op: str) -> Callable[[Any, Any], Any]:
        """Create a comparison method for the given operator."""
        return lambda self, other: _compare(self, other, op)

    # Assign comparison methods - mypy doesn't like assigning to special methods
    version_info.__lt__ = make_comparator("<")
    version_info.__le__ = make_comparator("<=")
    version_info.__gt__ = make_comparator(">")
    version_info.__ge__ = make_comparator(">=")
    version_info.__eq__ = make_comparator("==")  # type: ignore[method-assign,assignment]
    version_info.__ne__ = make_comparator("!=")  # type: ignore[method-assign,assignment]

    return version_info
