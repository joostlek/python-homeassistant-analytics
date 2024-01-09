"""Asynchronous Python client for Homeassistant Analytics."""
from aioresponses import aioresponses

from tests.const import HOMEASSISTANT_ANALYTICS_URL

from pathlib import Path


def load_fixture(filename: str) -> str:
    """Load a fixture."""
    path = Path(__package__) / "fixtures" / filename
    return path.read_text(encoding="utf-8")
