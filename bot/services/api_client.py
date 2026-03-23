"""
LMS API Client

Handles all communication with the LMS backend.
Uses Bearer token authentication and provides user-friendly error messages.
"""

import httpx
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings


class LMSClient:
    """Client for the LMS backend API."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        """Initialize the LMS client.

        Args:
            base_url: Override for the API base URL (uses config by default)
            api_key: Override for the API key (uses config by default)
        """
        self.base_url = (base_url or settings.lms_api_base_url).rstrip("/")
        self.api_key = api_key or settings.lms_api_key

    def _get_headers(self) -> dict[str, str]:
        """Get headers for authenticated requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def get_items(self) -> list[dict]:
        """Fetch all items (labs and tasks) from the backend.

        Returns:
            List of item dictionaries

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/items/"
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()

    def get_learners(self) -> list[dict]:
        """Fetch all enrolled learners.

        Returns:
            List of learner dictionaries

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/learners/"
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()

    def get_scores(self, lab: str) -> list[dict]:
        """Fetch score distribution for a specific lab.

        Args:
            lab: The lab identifier (e.g., "lab-04")

        Returns:
            List of score bucket dictionaries

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/analytics/scores"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()

    def get_pass_rates(self, lab: str) -> list[dict]:
        """Fetch pass rates for a specific lab.

        Args:
            lab: The lab identifier (e.g., "lab-04")

        Returns:
            List of pass rate dictionaries

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/analytics/pass-rates"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()

    def get_timeline(self, lab: str) -> list[dict]:
        """Fetch submission timeline for a specific lab.

        Args:
            lab: The lab identifier (e.g., "lab-04")

        Returns:
            List of timeline entries (date, submissions)

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/analytics/timeline"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()

    def get_groups(self, lab: str) -> list[dict]:
        """Fetch per-group performance data for a specific lab.

        Args:
            lab: The lab identifier (e.g., "lab-04")

        Returns:
            List of group performance dictionaries

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/analytics/groups"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()

    def get_top_learners(self, lab: str, limit: int = 5) -> list[dict]:
        """Fetch top N learners for a specific lab.

        Args:
            lab: The lab identifier (e.g., "lab-04")
            limit: Number of top learners to return

        Returns:
            List of top learner dictionaries

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/analytics/top-learners"
        params = {"lab": lab, "limit": limit}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()

    def get_completion_rate(self, lab: str) -> dict:
        """Fetch completion rate for a specific lab.

        Args:
            lab: The lab identifier (e.g., "lab-04")

        Returns:
            Completion rate dictionary

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/analytics/completion-rate"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()

    def trigger_sync(self) -> dict:
        """Trigger a data sync from the autochecker.

        Returns:
            Sync result dictionary

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/pipeline/sync"
        with httpx.Client() as client:
            response = client.post(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()


def format_error_message(error: Exception) -> str:
    """Format an HTTP error into a user-friendly message.

    Args:
        error: The exception that occurred

    Returns:
        A user-friendly error message that includes the actual error
    """
    if isinstance(error, httpx.ConnectError):
        # Extract the host/port from the error if possible
        error_str = str(error)
        if "localhost:42002" in error_str or "Connection refused" in error_str:
            return f"Backend error: connection refused (localhost:42002). Check that the services are running."
        return f"Backend error: {error_str}. Check that the backend is running."

    if isinstance(error, httpx.HTTPStatusError):
        status = error.response.status_code
        reason = error.response.reason_phrase
        return f"Backend error: HTTP {status} {reason}. The backend service may be down."

    if isinstance(error, httpx.RequestError):
        return f"Backend error: {str(error)}. Check your network connection."

    # Generic fallback that still shows the error
    return f"Backend error: {str(error)}"


# Global client instance
lms_client = LMSClient()
