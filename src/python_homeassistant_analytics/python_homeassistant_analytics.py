"""Homeassistant Client."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from importlib import metadata
from typing import Self

from aiohttp import ClientConnectionError, ClientSession
import orjson
from yarl import URL

from python_homeassistant_analytics.exceptions import (
    HomeassistantAnalyticsConnectionError,
    HomeassistantAnalyticsError,
    HomeassistantAnalyticsNotModifiedError,
)
from python_homeassistant_analytics.models import (
    Addon,
    Analytics,
    CurrentAnalytics,
    CustomIntegration,
    Integration,
)

VERSION = metadata.version(__package__)


@dataclass
class HomeassistantAnalyticsClient:
    """Main class for handling connections with Homeassistant Analytics."""

    session: ClientSession | None = None
    request_timeout: int = 10
    api_host: str = "analytics.home-assistant.io"
    _close_session: bool = False
    _etags: dict[str, str] = field(default_factory=dict)

    async def _request(self, host: str, uri: str) -> str:
        """Handle a request to Homeassistant Analytics."""
        url = URL.build(
            scheme="https",
            host=host,
            port=443,
        ).joinpath(uri)

        headers = {
            "User-Agent": f"PythonHomeassistantAnalytics/{VERSION}",
            "Accept": "application/json, text/plain, */*",
        }
        if etag := self._etags.get(url.path):
            headers["If-None-Match"] = etag

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.get(
                    url,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to Homeassistant Analytics"
            raise HomeassistantAnalyticsConnectionError(msg) from exception
        except ClientConnectionError as exception:
            msg = "Error occurred while connecting to Homeassistant Analytics"
            raise HomeassistantAnalyticsConnectionError(msg) from exception

        content_type = response.headers.get("Content-Type", "")

        if response.status == 304:
            raise HomeassistantAnalyticsNotModifiedError

        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected response from Homeassistant Analytics"
            raise HomeassistantAnalyticsError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        if etag := response.headers.get("etag"):
            self._etags[url.path] = etag

        return await response.text()

    async def get_analytics(self) -> Analytics:
        """Get analytics."""
        response = await self._request("analytics.home-assistant.io", "data.json")
        return Analytics.from_json(response)

    async def get_current_analytics(self) -> CurrentAnalytics:
        """Get current analytics."""
        response = await self._request(
            "analytics.home-assistant.io",
            "current_data.json",
        )
        return CurrentAnalytics.from_json(response)

    async def get_integrations(self) -> dict[str, Integration]:
        """Get integrations."""
        response = await self._request("home-assistant.io", "integrations.json")
        obj = orjson.loads(response)  # pylint: disable=no-member
        return {key: Integration.from_dict(value) for key, value in obj.items()}

    async def get_addons(self) -> dict[str, Addon]:
        """Get addons."""
        response = await self._request("analytics.home-assistant.io", "addons.json")
        obj = orjson.loads(response)  # pylint: disable=no-member
        return {key: Addon.from_dict(value) for key, value in obj.items()}

    async def get_custom_integrations(self) -> dict[str, CustomIntegration]:
        """Get custom integrations."""
        response = await self._request(
            "analytics.home-assistant.io",
            "custom_integrations.json",
        )
        obj = orjson.loads(response)  # pylint: disable=no-member
        return {key: CustomIntegration.from_dict(value) for key, value in obj.items()}

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The HomeassistantAnalyticsClient object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
