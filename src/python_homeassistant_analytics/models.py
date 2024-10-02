"""Models for Homeassistant Analytics."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class InstallationTypes(DataClassORJSONMixin):
    """InstallationTypes model."""

    os: int
    container: int
    core: int
    supervised: int
    unsupported_container: int
    unknown: int


@dataclass
class CurrentAnalytics(DataClassORJSONMixin):
    """CurrentAnalytics model."""

    last_updated: datetime = field(
        metadata=field_options(
            deserialize=lambda x: datetime.fromtimestamp(x / 1000, tz=timezone.utc),
        ),
    )
    countries: dict[str, int]
    installation_types: InstallationTypes
    active_installations: int
    average_users: int = field(metadata=field_options(alias="avg_users"))
    average_automations: int = field(metadata=field_options(alias="avg_automations"))
    average_integrations: int = field(metadata=field_options(alias="avg_integrations"))
    average_addons: int = field(metadata=field_options(alias="avg_addons"))
    average_states: int = field(metadata=field_options(alias="avg_states"))
    integrations: dict[str, int]
    reports_integrations: int


@dataclass
class Analytics(DataClassORJSONMixin):
    """Analytics model."""

    current: CurrentAnalytics = field(metadata=field_options(alias="current"))


class IntegrationType(StrEnum):
    """Integration type."""

    INTEGRATION = "integration"
    VIRTUAL = "virtual"
    SERVICE = "service"
    ENTITY = "entity"
    HUB = "hub"
    DEVICE = "device"
    SYSTEM = "system"
    HELPER = "helper"
    BRAND = "brand"
    HARDWARE = "hardware"


@dataclass
class Integration(DataClassORJSONMixin):
    """Integration model."""

    title: str
    integration_type: IntegrationType


@dataclass
class CustomIntegration(DataClassORJSONMixin):
    """CustomIntegration model."""

    total: int
    versions: dict[str, int]


@dataclass
class Addon(DataClassORJSONMixin):
    """Addon model."""

    total: int
    versions: dict[str, int]
