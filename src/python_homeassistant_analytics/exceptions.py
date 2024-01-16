"""Asynchronous Python client for Homeassistant Analytics."""


class HomeassistantAnalyticsError(Exception):
    """Generic exception."""


class HomeassistantAnalyticsConnectionError(HomeassistantAnalyticsError):
    """Homeassistant Analytics connection exception."""


class HomeassistantAnalyticsNotModifiedError(HomeassistantAnalyticsError):
    """Homeassistant Analytics not modified exception."""
