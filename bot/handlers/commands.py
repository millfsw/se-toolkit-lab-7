"""
Command handlers implementation.

Each handler is a pure function that takes command arguments and returns a text response.
No Telegram dependencies here - same function works from --test mode or Telegram.
"""


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
    # TODO: Task 2 - call backend API
    return "Backend status: OK (placeholder - will check real backend in Task 2)"


def handle_labs() -> str:
    """Handle /labs command - list available labs."""
    # TODO: Task 2 - call backend API
    return "Available labs: (placeholder - will fetch from backend in Task 2)"


def handle_scores(lab: str = "") -> str:
    """Handle /scores command - view lab scores.
    
    Args:
        lab: The lab identifier (e.g., "lab-04")
    """
    if not lab:
        return "Please specify a lab, e.g., /scores lab-04"
    
    # TODO: Task 2 - call backend API
    return f"Scores for {lab}: (placeholder - will fetch from backend in Task 2)"
