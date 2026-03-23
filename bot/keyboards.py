"""
Inline keyboard definitions for the Telegram bot.

These keyboards provide quick action buttons for common queries.
The keyboards are defined separately from handlers to maintain separation of concerns.
"""


def get_start_keyboard() -> list[list[dict]]:
    """Get the inline keyboard for /start command.

    Returns:
        Inline keyboard markup as a list of button rows
    """
    return [
        [
            {"text": "📚 View Labs", "callback_data": "view_labs"},
            {"text": "🏥 Health Check", "callback_data": "health_check"},
        ],
        [
            {"text": "📊 Lab Scores", "callback_data": "scores_lab-01"},
            {"text": "📈 Pass Rates", "callback_data": "pass_rates_lab-01"},
        ],
        [
            {"text": "👥 Top Learners", "callback_data": "top_learners_lab-01"},
            {"text": "📅 Timeline", "callback_data": "timeline_lab-01"},
        ],
        [
            {"text": "❓ Help", "callback_data": "help"},
        ],
    ]


def get_lab_selection_keyboard() -> list[list[dict]]:
    """Get the inline keyboard for selecting a lab.

    Returns:
        Inline keyboard markup with lab buttons
    """
    return [
        [
            {"text": "Lab 01", "callback_data": "select_lab-01"},
            {"text": "Lab 02", "callback_data": "select_lab-02"},
            {"text": "Lab 03", "callback_data": "select_lab-03"},
        ],
        [
            {"text": "Lab 04", "callback_data": "select_lab-04"},
            {"text": "Lab 05", "callback_data": "select_lab-05"},
            {"text": "Lab 06", "callback_data": "select_lab-06"},
        ],
        [
            {"text": "Lab 07", "callback_data": "select_lab-07"},
        ],
    ]


def get_analytics_keyboard(lab_id: str = "lab-01") -> list[list[dict]]:
    """Get the inline keyboard for analytics actions on a specific lab.

    Args:
        lab_id: The lab identifier to use in callback data

    Returns:
        Inline keyboard markup with analytics buttons
    """
    return [
        [
            {"text": "📊 Scores", "callback_data": f"scores_{lab_id}"},
            {"text": "📈 Pass Rates", "callback_data": f"pass_rates_{lab_id}"},
        ],
        [
            {"text": "👥 Groups", "callback_data": f"groups_{lab_id}"},
            {"text": "🏆 Top Learners", "callback_data": f"top_learners_{lab_id}"},
        ],
        [
            {"text": "📅 Timeline", "callback_data": f"timeline_{lab_id}"},
            {"text": "✅ Completion", "callback_data": f"completion_{lab_id}"},
        ],
        [
            {"text": "🔙 Back to Labs", "callback_data": "view_labs"},
        ],
    ]
