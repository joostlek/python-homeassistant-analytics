"""Models for Homeassistant Analytics."""
from __future__ import annotations

from dataclasses import dataclass, field

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
