"""Common types for runnable examples."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class ExampleOptions:
    """Options passed from the CLI to every example."""

    query: str | None = None  # replaces the example's default user input
    model: str | None = None  # "provider:model" override, e.g. "openai:gpt-4o-mini"
    require_approval: bool = True  # human-in-the-loop prompts (sections 10, 12)


ExampleRunner = Callable[[ExampleOptions], Awaitable[None]]


@dataclass(frozen=True)
class Example:
    id: str  # lab section number, e.g. "05"
    slug: str  # CLI-friendly name, e.g. "minimal-agent"
    title: str
    concept: str  # the BeeAI concept this example introduces
    original_script: str  # the lab file it replaces, e.g. "t5.py"
    run: ExampleRunner
    interactive: bool = False  # asks for terminal input while running
