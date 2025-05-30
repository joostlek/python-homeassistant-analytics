"""Asynchronous Python client for Homeassistant Analytics."""

import asyncio
from typing import Any

import aiohttp
from aiohttp.hdrs import METH_GET
from aioresponses import CallbackResult, aioresponses
import pytest

from python_homeassistant_analytics import (
    Environment,
    HomeassistantAnalyticsClient,
    HomeassistantAnalyticsConnectionError,
    HomeassistantAnalyticsError,
    HomeassistantAnalyticsNotModifiedError,
)
from syrupy import SnapshotAssertion
from tests import load_fixture

from .const import HEADERS, HOMEASSISTANT_ANALYTICS_URL, HOMEASSISTANT_URL


async def test_putting_in_own_session(
    responses: aioresponses,
) -> None:
    """Test putting in own session."""
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/data.json",
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
        f"{HOMEASSISTANT_ANALYTICS_URL}/data.json",
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
        f"{HOMEASSISTANT_ANALYTICS_URL}/data.json",
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
        f"{HOMEASSISTANT_ANALYTICS_URL}/data.json",
        callback=response_handler,
    )
    async with HomeassistantAnalyticsClient(
        request_timeout=1,
    ) as homeassistant_analytics_client:
        with pytest.raises(HomeassistantAnalyticsConnectionError):
            assert await homeassistant_analytics_client.get_analytics()


@pytest.mark.usefixtures("responses")
async def test_client_connection_error() -> None:
    """Test client connection error."""
    async with HomeassistantAnalyticsClient() as homeassistant_analytics_client:
        with pytest.raises(HomeassistantAnalyticsConnectionError):
            assert await homeassistant_analytics_client.get_analytics()


async def test_analytics(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving analytics."""
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/data.json",
        status=200,
        body=load_fixture("data.json"),
    )
    assert await homeassistant_analytics_client.get_analytics() == snapshot


async def test_etags(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
) -> None:
    """Test retrieving current analytics."""
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/current_data.json",
        status=200,
        body=load_fixture("current_data.json"),
        headers={"etag": "123"},
    )
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/current_data.json",
        status=304,
    )

    assert await homeassistant_analytics_client.get_current_analytics()

    responses.assert_called_with(
        f"{HOMEASSISTANT_ANALYTICS_URL}/current_data.json",
        METH_GET,
        headers=HEADERS,
    )
    with pytest.raises(HomeassistantAnalyticsNotModifiedError):
        assert await homeassistant_analytics_client.get_current_analytics()

    responses.assert_called_with(
        f"{HOMEASSISTANT_ANALYTICS_URL}/current_data.json",
        METH_GET,
        headers={**HEADERS, "If-None-Match": "123"},
    )


async def test_current_analytics(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving current analytics."""
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/current_data.json",
        status=200,
        body=load_fixture("current_data.json"),
    )
    assert await homeassistant_analytics_client.get_current_analytics() == snapshot


async def test_integrations(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving integrations."""
    responses.get(
        f"{HOMEASSISTANT_URL}/integrations.json",
        status=200,
        body=load_fixture("integrations.json"),
    )
    assert await homeassistant_analytics_client.get_integrations() == snapshot


async def test_custom_integrations(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving custom integrations."""
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/custom_integrations.json",
        status=200,
        body=load_fixture("custom_integrations.json"),
    )
    assert await homeassistant_analytics_client.get_custom_integrations() == snapshot


async def test_addons(
    responses: aioresponses,
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test retrieving addons."""
    responses.get(
        f"{HOMEASSISTANT_ANALYTICS_URL}/addons.json",
        status=200,
        body=load_fixture("addons.json"),
    )
    assert await homeassistant_analytics_client.get_addons() == snapshot


@pytest.mark.parametrize(
    ("environment", "url"),
    [
        (None, f"{HOMEASSISTANT_URL}/integrations.json"),
        (Environment.CURRENT, f"{HOMEASSISTANT_URL}/integrations.json"),
        (Environment.RC, "https://rc.home-assistant.io/integrations.json"),
        (Environment.NEXT, "https://next.home-assistant.io/integrations.json"),
    ],
)
async def test_integration_environment(
    homeassistant_analytics_client: HomeassistantAnalyticsClient,
    responses: aioresponses,
    environment: Environment,
    url: str,
) -> None:
    """Test retrieving integrations from different environments."""
    responses.get(
        url,
        status=200,
        body=load_fixture("integrations.json"),
    )
    assert await homeassistant_analytics_client.get_integrations(environment)

    responses.assert_called_with(
        url,
        METH_GET,
        headers=HEADERS,
    )
