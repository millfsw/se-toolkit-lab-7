"""
LLM Client for tool-based routing.

Handles communication with the LLM API for intent recognition and tool calling.
Uses the OpenAI-compatible API format.
"""

import json
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from config import settings


class LLMClient:
    """Client for LLM API with tool calling support."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        """Initialize the LLM client.

        Args:
            api_key: Override for API key (uses config by default)
            base_url: Override for base URL (uses config by default)
            model: Override for model name (uses config by default)
        """
        self.api_key = api_key or settings.llm_api_key
        self.base_url = (base_url or settings.llm_api_base_url).rstrip("/")
        self.model = model or settings.llm_api_model

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        """Send a chat request to the LLM.

        Args:
            messages: List of message dicts with role and content
            tools: Optional list of tool definitions

        Returns:
            The LLM response dict

        Raises:
            httpx.RequestError: If the request fails
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    def extract_tool_calls(self, response: dict) -> list[dict]:
        """Extract tool calls from an LLM response.

        Args:
            response: The LLM response dict

        Returns:
            List of tool call dicts with name and arguments
        """
        choices = response.get("choices", [])
        if not choices:
            return []

        message = choices[0].get("message", {})
        tool_calls = message.get("tool_calls", [])

        result = []
        for call in tool_calls:
            function = call.get("function", {})
            try:
                arguments = json.loads(function.get("arguments", "{}"))
            except json.JSONDecodeError:
                arguments = {}

            result.append({
                "id": call.get("id"),
                "name": function.get("name"),
                "arguments": arguments,
            })

        return result

    def get_response_text(self, response: dict) -> str:
        """Extract response text from an LLM response.

        Args:
            response: The LLM response dict

        Returns:
            The response text
        """
        choices = response.get("choices", [])
        if not choices:
            return ""

        message = choices[0].get("message", {})
        return message.get("content", "")


# Global client instance
llm_client = LLMClient()
