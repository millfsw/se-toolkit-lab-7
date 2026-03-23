"""
Command handlers implementation.

Each handler is a pure function that takes command arguments and returns a text response.
No Telegram dependencies here - same function works from --test mode or Telegram.
"""

import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from services.api_client import lms_client, format_error_message


def handle_start() -> str:
    """Handle /start command - welcome message."""
    return "Welcome to the LMS Bot! I can help you check system health, browse labs, view scores, and answer questions. Use /help to see all available commands."


def handle_help() -> str:
    """Handle /help command - list available commands."""
    return """Available commands:
/start - Welcome message
/help - Show this help message
/health - Check backend system status
/labs - List available labs
/scores <lab> - View scores for a specific lab

You can also ask questions in plain language (coming soon)."""


def handle_health() -> str:
    """Handle /health command - check backend status."""
    try:
        items = lms_client.get_items()
        return f"Backend is healthy. {len(items)} items available."
    except Exception as e:
        return format_error_message(e)


def handle_labs() -> str:
    """Handle /labs command - list available labs."""
    try:
        items = lms_client.get_items()
        labs = [item for item in items if item.get("type") == "lab"]
        
        if not labs:
            return "No labs found in the backend."
        
        lines = ["Available labs:"]
        for lab in labs:
            lab_id = lab.get("id", "")
            title = lab.get("title", "Unknown")
            lines.append(f"- {title}")
        
        return "\n".join(lines)
    except Exception as e:
        return format_error_message(e)


def handle_scores(lab: str = "") -> str:
    """Handle /scores command - view lab scores.

    Args:
        lab: The lab identifier (e.g., "lab-04")
    """
    if not lab:
        return "Please specify a lab, e.g., /scores lab-04"

    try:
        pass_rates = lms_client.get_pass_rates(lab)
        
        if not pass_rates:
            return f"No pass rates found for '{lab}'. Check the lab identifier."
        
        lines = [f"Pass rates for {lab}:"]
        for rate in pass_rates:
            task_name = rate.get("task", "Unknown task")
            avg_score = rate.get("avg_score", 0)  # Already a percentage (0-100)
            attempts = rate.get("attempts", 0)
            lines.append(f"- {task_name}: {avg_score:.1f}% ({attempts} attempts)")
        
        return "\n".join(lines)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Lab '{lab}' not found. Use /labs to see available labs."
        return format_error_message(e)
    except Exception as e:
        return format_error_message(e)
