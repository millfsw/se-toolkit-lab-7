"""
Command handlers for the Telegram bot.

Handlers are pure functions that take input and return text responses.
They have no dependency on Telegram, making them testable in isolation.
The same handler functions work from --test mode, unit tests, or Telegram.
"""

from .commands import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)
from .keyboards import (
    get_start_keyboard,
    get_lab_selection_keyboard,
    get_analytics_keyboard,
)

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
    "get_start_keyboard",
    "get_lab_selection_keyboard",
    "get_analytics_keyboard",
]
