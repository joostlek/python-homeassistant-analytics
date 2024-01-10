"""Constants for tests."""
from importlib import metadata

HOMEASSISTANT_ANALYTICS_URL = "https://analytics.home-assistant.io:443"

version = metadata.version("python_homeassistant_analytics")

HEADERS = {
    "User-Agent": f"PythonHomeassistantAnalytics/{version}",
    "Accept": "application/json, text/plain, */*",
}
