"""
LMS Telegram Bot - Entry Point

Usage:
    uv run bot.py              # Run as Telegram bot
    uv run bot.py --test "/command"  # Test mode (no Telegram connection)
"""

import argparse
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)


def parse_command(text: str) -> tuple[str, str]:
    """Parse a command string into command and arguments.
    
    Args:
        text: The input text (e.g., "/scores lab-04" or "/start")
    
    Returns:
        Tuple of (command, arguments)
    """
    text = text.strip()
    if not text.startswith("/"):
        # Plain text query (for Task 3 - natural language)
        return "", text
    
    parts = text[1:].split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return command, args


def run_command(command: str, args: str) -> str:
    """Execute a command and return the response.
    
    Args:
        command: The command name (without /)
        args: Command arguments
    
    Returns:
        The response text
    """
    handlers = {
        "start": handle_start,
        "help": handle_help,
        "health": handle_health,
        "labs": handle_labs,
    }
    
    if command in handlers:
        return handlers[command]()
    elif command == "scores":
        return handle_scores(args)
    else:
        return f"Unknown command: /{command}. Use /help to see available commands."


def run_test_mode(query: str) -> None:
    """Run a command in test mode (no Telegram connection).
    
    Args:
        query: The command or text to test (e.g., "/start" or "what labs are available")
    """
    command, args = parse_command(query)
    
    if command:
        # Slash command
        response = run_command(command, args)
    else:
        # Plain text query (Task 3 - will use LLM)
        response = f"Plain text query: '{args}' - LLM routing coming in Task 3"
    
    print(response)


def run_telegram_bot() -> None:
    """Run the bot with Telegram connection.
    
    This will be implemented in Task 2 when we add the aiogram integration.
    """
    from config import settings
    
    if not settings.bot_token:
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        print("Cannot start Telegram bot without a token.")
        print("For testing, use: uv run bot.py --test '/start'")
        sys.exit(1)
    
    # TODO: Task 2 - implement Telegram bot with aiogram
    print("Telegram bot starting... (implementation coming in Task 2)")
    print(f"Bot token configured: {bool(settings.bot_token)}")
    print(f"LMS API URL: {settings.lms_api_base_url}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="LMS Telegram Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    uv run bot.py --test "/start"         Test /start command
    uv run bot.py --test "/health"        Test /health command
    uv run bot.py --test "/scores lab-04" Test /scores with argument
    uv run bot.py                         Run as Telegram bot
""",
    )
    parser.add_argument(
        "--test",
        type=str,
        metavar="QUERY",
        help="Test mode: run a command without connecting to Telegram",
    )
    
    args = parser.parse_args()
    
    if args.test:
        run_test_mode(args.test)
    else:
        run_telegram_bot()


if __name__ == "__main__":
    main()
