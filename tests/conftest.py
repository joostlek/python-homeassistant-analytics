"""Asynchronous Python client for Homeassistant Analytics."""

from collections.abc import AsyncGenerator

import aiohttp
from aiointercept import aiointercept
import pytest

from python_homeassistant_analytics import HomeassistantAnalyticsClient
from syrupy import SnapshotAssertion

from .syrupy import HomeassistantAnalyticsSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Homeassistant Analytics extension."""
    return snapshot.use_extension(HomeassistantAnalyticsSnapshotExtension)


@pytest.fixture(name="homeassistant_analytics_client")
async def client() -> AsyncGenerator[HomeassistantAnalyticsClient]:
    """Return a Spotify client."""
    async with (
        aiohttp.ClientSession() as session,
        HomeassistantAnalyticsClient(
            session=session,
        ) as homeassistant_analytics_client,
    ):
        yield homeassistant_analytics_client


@pytest.fixture(name="responses")
async def aiointercept_fixture() -> AsyncGenerator[aiointercept]:
    """Return aiointercept fixture."""
    async with aiointercept(mock_external_urls=True) as mocked_responses:
        yield mocked_responses
