# Bot Development Plan

## Overview

This document outlines the development plan for building a Telegram bot that interfaces with the LMS (Learning Management System) backend. The bot enables users to check system health, browse available labs, view scores, and ask questions in natural language.

## Architecture

The bot follows a layered architecture with clear separation of concerns:

1. **Entry Point (`bot.py`)**: Handles Telegram connection and CLI test mode. Routes incoming messages to the appropriate handlers.
2. **Handlers (`handlers/`)**: Pure functions that implement command logic. They take input and return text responses without any Telegram dependency. This makes them testable in isolation.
3. **Services (`services/`)**: External API clients (LMS backend, LLM) that handle HTTP communication, authentication, and response parsing.
4. **Configuration (`config.py`)**: Centralized environment variable loading using pydantic-settings for type safety and validation.

## Task 1: Project Scaffold

Create the basic project structure with testable handlers and a `--test` mode. The entry point supports running commands directly from the command line without connecting to Telegram. Handlers return placeholder text. This establishes the foundation for iterative development.

## Task 2: Backend Integration

Replace placeholder handlers with real API calls. Implement an HTTP client service that communicates with the LMS backend using Bearer token authentication. Commands like `/health`, `/labs`, and `/scores` fetch actual data from the backend. Error handling ensures graceful degradation when the backend is unavailable.

## Task 3: Intent-Based Natural Language Routing

Add LLM-powered intent recognition. Instead of requiring slash commands, users can ask questions in plain language. The LLM analyzes the query and selects the appropriate tool (handler) to execute. Tool descriptions must be clear and specific so the LLM understands when to use each one. This enables conversational interactions like "what labs are available?" instead of requiring `/labs`.

## Task 4: Containerization and Deployment

Create a Dockerfile for the bot and add it as a service in docker-compose.yml. Configure proper networking so the bot can reach the backend using service names instead of localhost. Document the deployment process and verify the bot works in production. Set up health checks and logging for monitoring.

## Testing Strategy

- **Unit tests**: Test individual handlers with mocked services
- **Integration tests**: Test the full flow from Telegram message to backend query
- **Test mode**: Use `--test` flag for quick manual verification during development
- **End-to-end**: Deploy to VM and verify real Telegram interaction

## Dependencies

- `aiogram`: Async Telegram bot framework
- `httpx`: Async HTTP client for API calls
- `pydantic-settings`: Type-safe configuration management
- LLM client: For natural language intent recognition (Task 3)

## Environment Variables

- `BOT_TOKEN`: Telegram bot authentication token
- `LMS_API_BASE_URL`: Base URL for the LMS backend
- `LMS_API_KEY`: Bearer token for backend authentication
- `LLM_API_KEY`: API key for the LLM service
- `LLM_API_BASE_URL`: Base URL for the LLM service
- `LLM_API_MODEL`: Model name for intent recognition
