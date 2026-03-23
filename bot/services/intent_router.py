"""
Intent Router for natural language queries.

Routes user messages to the appropriate backend tools via LLM.
Implements the tool calling loop:
1. Send message + tools to LLM
2. LLM returns tool calls
3. Execute tools
4. Feed results back to LLM
5. LLM produces final answer
"""

import json
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.llm_client import llm_client
from services.api_client import lms_client, format_error_message
from services.tools import TOOLS, SYSTEM_PROMPT


def execute_tool(name: str, arguments: dict) -> str:
    """Execute a tool and return the result as a string.

    Args:
        name: The tool name
        arguments: Tool arguments

    Returns:
        JSON string of the result
    """
    try:
        if name == "get_items":
            result = lms_client.get_items()
        elif name == "get_learners":
            result = lms_client.get_learners()
        elif name == "get_scores":
            lab = arguments.get("lab", "")
            result = lms_client.get_scores(lab)
        elif name == "get_pass_rates":
            lab = arguments.get("lab", "")
            result = lms_client.get_pass_rates(lab)
        elif name == "get_timeline":
            lab = arguments.get("lab", "")
            result = lms_client.get_timeline(lab)
        elif name == "get_groups":
            lab = arguments.get("lab", "")
            result = lms_client.get_groups(lab)
        elif name == "get_top_learners":
            lab = arguments.get("lab", "")
            limit = arguments.get("limit", 5)
            result = lms_client.get_top_learners(lab, limit)
        elif name == "get_completion_rate":
            lab = arguments.get("lab", "")
            result = lms_client.get_completion_rate(lab)
        elif name == "trigger_sync":
            result = lms_client.trigger_sync()
        else:
            result = {"error": f"Unknown tool: {name}"}

        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": format_error_message(e)})


def route(user_message: str) -> str:
    """Route a user message through the LLM to get a response.

    Args:
        user_message: The user's natural language query

    Returns:
        The bot's response
    """
    # Initialize conversation with system prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    max_iterations = 5  # Prevent infinite loops
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Call LLM
        try:
            response = llm_client.chat(messages, tools=TOOLS)
        except Exception as e:
            return f"LLM error: {format_error_message(e)}"

        # Extract tool calls
        tool_calls = llm_client.extract_tool_calls(response)

        if not tool_calls:
            # No tool calls - LLM has a final answer
            return llm_client.get_response_text(response)

        # Debug: print tool calls to stderr
        for call in tool_calls:
            print(f"[tool] LLM called: {call['name']}({call['arguments']})", file=sys.stderr)

        # Execute tools and collect results
        tool_results = []
        for call in tool_calls:
            result = execute_tool(call["name"], call["arguments"])
            print(f"[tool] Result: {result[:100]}...", file=sys.stderr)

            tool_results.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": result,
            })

        # Add assistant's message with tool calls to conversation
        assistant_message = response.get("choices", [{}])[0].get("message", {})
        # Remove content if it's None to avoid issues
        if assistant_message.get("content") is None:
            assistant_message["content"] = ""
        
        # Ensure tool_calls have proper format for Qwen
        if "tool_calls" in assistant_message:
            for tc in assistant_message["tool_calls"]:
                if "type" not in tc:
                    tc["type"] = "function"
                if "function" in tc:
                    if "arguments" in tc["function"] and isinstance(tc["function"]["arguments"], dict):
                        tc["function"]["arguments"] = json.dumps(tc["function"]["arguments"])
        
        messages.append(assistant_message)

        # Add tool results to conversation
        messages.extend(tool_results)

        print(f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM", file=sys.stderr)
        
        # Debug: show messages being sent
        print(f"[debug] Messages count: {len(messages)}", file=sys.stderr)
        
        # Debug: print last few messages
        for i, msg in enumerate(messages[-2:], start=len(messages)-2):
            role = msg.get("role", "unknown")
            content_preview = msg.get("content", "")[:50] if msg.get("content") else ""
            print(f"[debug] Message {i}: role={role}, content={content_preview}...", file=sys.stderr)

    return "I'm having trouble processing your request. Please try rephrasing."
