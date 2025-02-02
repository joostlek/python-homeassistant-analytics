"""Constants for tests."""

from importlib import metadata

HOMEASSISTANT_ANALYTICS_URL = "https://analytics.home-assistant.io"
HOMEASSISTANT_URL = "https://next.home-assistant.io"

version = metadata.version("python_homeassistant_analytics")

HEADERS = {
    "User-Agent": f"PythonHomeassistantAnalytics/{version}",
    "Accept": "application/json, text/plain, */*",
}
