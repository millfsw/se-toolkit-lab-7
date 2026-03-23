"""Services for the bot - API clients, LLM clients, etc."""

from .api_client import lms_client, LMSClient, format_error_message
from .llm_client import llm_client, LLMClient
from .tools import TOOLS, SYSTEM_PROMPT

__all__ = [
    "lms_client",
    "LMSClient",
    "format_error_message",
    "llm_client",
    "LLMClient",
    "TOOLS",
    "SYSTEM_PROMPT",
]
