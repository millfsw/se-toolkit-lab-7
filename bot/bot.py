"""
LMS Telegram Bot - Entry Point

Usage:
    uv run bot.py              # Run as Telegram bot
    uv run bot.py --test "/command"  # Test mode (no Telegram connection)
"""

import argparse
import asyncio
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
    get_start_keyboard,
)
from services.intent_router import route as route_intent


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
        # Plain text query - use LLM intent router
        response = route_intent(args)

    print(response)


async def run_telegram_bot() -> None:
    """Run the bot with Telegram connection using aiogram."""
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import Command
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from config import settings

    if not settings.bot_token:
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        print("Cannot start Telegram bot without a token.")
        print("For testing, use: uv run bot.py --test '/start'")
        sys.exit(1)

    # Initialize bot and dispatcher
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # Build inline keyboard from keyboard definitions
    def build_keyboard(keyboard_def: list[list[dict]]) -> InlineKeyboardMarkup:
        """Convert keyboard definition to aiogram InlineKeyboardMarkup."""
        keyboard = []
        for row in keyboard_def:
            keyboard_row = []
            for button in row:
                keyboard_row.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=button["callback_data"],
                    )
                )
            keyboard.append(keyboard_row)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        """Handle /start command with inline keyboard."""
        text = handle_start()
        keyboard = build_keyboard(get_start_keyboard())
        await message.answer(text, reply_markup=keyboard)

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        """Handle /help command."""
        await message.answer(handle_help())

    @dp.message(Command("health"))
    async def cmd_health(message: types.Message):
        """Handle /health command."""
        await message.answer(handle_health())

    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message):
        """Handle /labs command."""
        await message.answer(handle_labs())

    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message):
        """Handle /scores command with lab argument."""
        # Get the lab argument from the command
        args = message.text.split(maxsplit=1)
        lab = args[1] if len(args) > 1 else ""
        await message.answer(handle_scores(lab))

    @dp.callback_query()
    async def handle_callback(callback_query: types.CallbackQuery):
        """Handle inline keyboard button clicks."""
        data = callback_query.data
        await callback_query.answer()  # Acknowledge the callback

        # Route based on callback data
        if data == "view_labs":
            await callback_query.message.answer(handle_labs())
        elif data == "health_check":
            await callback_query.message.answer(handle_health())
        elif data == "help":
            await callback_query.message.answer(handle_help())
        elif data.startswith("scores_"):
            lab = data.replace("scores_", "")
            await callback_query.message.answer(handle_scores(lab))
        elif data.startswith("pass_rates_"):
            lab = data.replace("pass_rates_", "")
            await callback_query.message.answer(handle_scores(lab))
        elif data.startswith("top_learners_"):
            lab = data.replace("top_learners_", "")
            # Use LLM to get top learners
            response = route_intent(f"top 5 students in {lab}")
            await callback_query.message.answer(response)
        elif data.startswith("timeline_"):
            lab = data.replace("timeline_", "")
            response = route_intent(f"show timeline for {lab}")
            await callback_query.message.answer(response)
        elif data.startswith("select_lab-"):
            lab = data.replace("select_lab-", "lab-")
            await callback_query.message.answer(
                f"You selected {lab}. What would you like to know about it?"
            )

    @dp.message()
    async def handle_message(message: types.Message):
        """Handle all other messages - use LLM intent routing."""
        text = message.text or ""

        if not text.strip():
            return

        # Use LLM to route the intent
        response = route_intent(text)
        await message.answer(response)

    # Start polling
    print("Telegram bot starting...")
    print(f"Bot token configured: {bool(settings.bot_token)}")
    print(f"LMS API URL: {settings.lms_api_base_url}")
    print(f"LLM API URL: {settings.llm_api_base_url}")
    print("Bot is running. Press Ctrl+C to stop.")

    await dp.start_polling(bot)


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
    uv run bot.py --test "what labs"      Test natural language query
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
        asyncio.run(run_telegram_bot())


if __name__ == "__main__":
    main()
