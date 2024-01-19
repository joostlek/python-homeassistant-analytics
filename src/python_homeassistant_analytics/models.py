"""Models for Homeassistant Analytics."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class CurrentAnalytics(DataClassORJSONMixin):
    """CurrentAnalytics model."""

    integrations: dict[str, int]


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
