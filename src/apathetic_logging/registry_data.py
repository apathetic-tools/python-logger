# src/apathetic_logging/registry_data.py
"""Registry for configurable log level settings."""

from __future__ import annotations


class ApatheticLogging_Internal_RegistryData:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides registry storage for configurable settings.

    This class contains class-level attributes for storing registered configuration
    values. When mixed into apathetic_logging, it provides centralized storage for
    log level environment variables, default log level, and logger name.

    Other mixins access these registries via direct class reference:
    ``ApatheticLogging_Internal_RegistryData.registered_internal_*``
    """

    # Registry for configurable log level settings
    # These are class-level attributes to avoid module-level namespace pollution
    # Public but marked with _internal_ to indicate internal use by other mixins
    registered_internal_log_level_env_vars: list[str] | None = None
    registered_internal_default_log_level: str | None = None
    registered_internal_logger_name: str | None = None
