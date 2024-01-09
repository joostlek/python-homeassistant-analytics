"""Asynchronous Python client for Homeassistant Analytics."""
from typing import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from python_homeassistant_analytics import HomeassistantAnalyticsClient
from syrupy import SnapshotAssertion

from .syrupy import HomeassistantAnalyticsSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Homeassistant Analytics extension."""
    return snapshot.use_extension(HomeassistantAnalyticsSnapshotExtension)


@pytest.fixture(name="homeassistant_analytics_client")
async def client() -> AsyncGenerator[HomeassistantAnalyticsClient, None]:
    """Return a Spotify client."""
    async with aiohttp.ClientSession() as session, HomeassistantAnalyticsClient(
        session=session,
    ) as homeassistant_analytics_client:
        yield homeassistant_analytics_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
