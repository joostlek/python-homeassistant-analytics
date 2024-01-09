"""Asynchronous Python client for Homeassistant Analytics."""
import asyncio
from typing import Any

import aiohttp
from aioresponses import CallbackResult, aioresponses
import pytest

from python_homeassistant_analytics import (
    HomeassistantAnalyticsClient,
    HomeassistantAnalyticsConnectionError,
    HomeassistantAnalyticsError,
)
from syrupy import SnapshotAssertion
from tests import load_fixture

from .const import HOMEASSISTANT_ANALYTICS_URL


async def test_putting_in_own_session(
    responses: aioresponses,
) -> None:
    """Test putting in own session."""
    responses.get(
        HOMEASSISTANT_ANALYTICS_URL,
        status=200,
        body=load_fixture("data.json"),
    )
    async with aiohttp.ClientSession() as session:
        analytics = HomeassistantAnalyticsClient(session=session)
        await analytics.get_analytics()
        assert analytics.session is not None
        assert not analytics.session.closed
        await analytics.close()
        assert not analytics.session.closed


async def test_creating_own_session(
    responses: aioresponses,
) -> None:
    """Test creating own session."""
    responses.get(
        HOMEASSISTANT_ANALYTICS_URL,
        status=200,
        body=load_fixture("data.json"),
    )
    analytics = HomeassistantAnalyticsClient()
    await analytics.get_analytics()
    assert analytics.session is not None
    assert not analytics.session.closed
    await analytics.close()
    assert analytics.session.closed


async def test_unexpected_server_response(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
) -> None:
    """Test handling unexpected response."""
    responses.get(
        HOMEASSISTANT_ANALYTICS_URL,
        status=200,
        headers={"Content-Type": "plain/text"},
        body="Yes",
    )
    with pytest.raises(HomeassistantAnalyticsError):
        assert await homeassistant_analytics_client.get_analytics()


async def test_timeout(
    responses: aioresponses,
) -> None:
    """Test request timeout."""

    # Faking a timeout by sleeping
    async def response_handler(_: str, **_kwargs: Any) -> CallbackResult:
        """Response handler for this test."""
        await asyncio.sleep(2)
        return CallbackResult(body="Goodmorning!")

    responses.get(
        HOMEASSISTANT_ANALYTICS_URL,
        callback=response_handler,
    )
    async with HomeassistantAnalyticsClient(
        request_timeout=1,
    ) as homeassistant_analytics_client:
        with pytest.raises(HomeassistantAnalyticsConnectionError):
            assert await homeassistant_analytics_client.get_analytics()


async def test_analytics(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving analytics."""
    responses.get(
        HOMEASSISTANT_ANALYTICS_URL,
        status=200,
        body=load_fixture("data.json"),
    )
    assert await homeassistant_analytics_client.get_analytics() == snapshot
