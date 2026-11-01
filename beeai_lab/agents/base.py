"""Shared agent builder.

Every agent in the lab is a ``RequirementAgent`` with ``UnconstrainedMemory``
and (from section 6 on) a ``GlobalTrajectoryMiddleware`` that prints each tool
call. :func:`build_agent` captures that pattern once.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.requirement import Requirement
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool


def tool_trajectory_middleware() -> GlobalTrajectoryMiddleware:
    """Middleware that logs every tool invocation to the console."""
    return GlobalTrajectoryMiddleware(included=[Tool])


def build_agent(
    llm: ChatModel,
    instructions: str,
    tools: Sequence[Tool[Any, Any, Any]] = (),
    requirements: Sequence[Requirement[Any]] = (),
    *,
    track_tools: bool = True,
) -> RequirementAgent:
    """Create a ``RequirementAgent`` with the lab's standard memory and middleware."""
    return RequirementAgent(
        llm=llm,
        tools=list(tools),
        memory=UnconstrainedMemory(),
        instructions=instructions,
        middlewares=[tool_trajectory_middleware()] if track_tools else [],
        requirements=list(requirements),
    )
