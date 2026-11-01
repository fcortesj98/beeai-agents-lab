"""Chat model factory — the single place where ``ChatModel`` objects are created."""

from __future__ import annotations

from beeai_framework.backend import ChatModel, ChatModelParameters

from beeai_lab.config import ModelSettings, get_settings, model_settings_for


def create_chat_model(settings: ModelSettings | str) -> ChatModel:
    """Create a BeeAI ``ChatModel`` from settings or a ``provider:model`` string."""
    if isinstance(settings, str):
        settings = model_settings_for(settings)
    if settings.temperature is None:
        return ChatModel.from_name(settings.name)
    return ChatModel.from_name(settings.name, ChatModelParameters(temperature=settings.temperature))


def chat_llm(override: str | None = None) -> ChatModel:
    """Model for plain chat and prompt templates (default: IBM Granite)."""
    return create_chat_model(override or get_settings().chat)


def structured_llm(override: str | None = None) -> ChatModel:
    """Model for structured output (default: OpenAI GPT-5 nano)."""
    return create_chat_model(override or get_settings().structured)


def agent_llm(override: str | None = None) -> ChatModel:
    """Model that powers the agents (default: Meta Llama 4 Maverick on watsonx)."""
    return create_chat_model(override or get_settings().agent)
