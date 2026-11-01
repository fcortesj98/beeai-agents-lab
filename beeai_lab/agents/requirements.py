"""Reusable requirement sets (lab sections 6-10).

Requirements are BeeAI's declarative rules for *when* and *how often* an agent
may call each tool. Each function below returns a fresh list so agents never
share requirement state.
"""

from __future__ import annotations

from typing import Any

from beeai_framework.agents.experimental.requirements.ask_permission import AskPermissionRequirement
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.agents.experimental.requirements.requirement import Requirement
from beeai_framework.tools import Tool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.think import ThinkTool

Requirements = list[Requirement[Any]]


def limited_research() -> Requirements:
    """Section 6: Wikipedia may be used, at most twice."""
    return [ConditionalRequirement(WikipediaTool, max_invocations=2)]


def limited_reasoning_and_research() -> Requirements:
    """Section 7: thinking and research both allowed, each at most twice."""
    return [
        ConditionalRequirement(ThinkTool, max_invocations=2),
        ConditionalRequirement(WikipediaTool, max_invocations=2),
    ]


def think_then_research(*, think_max: int = 3, research_min: int = 1, research_max: int = 2) -> Requirements:
    """Section 8: must think first (step 1), then research at least once."""
    return [
        ConditionalRequirement(
            ThinkTool,
            force_at_step=1,
            min_invocations=1,
            max_invocations=think_max,
            consecutive_allowed=False,
        ),
        ConditionalRequirement(
            WikipediaTool,
            only_after=[ThinkTool],
            min_invocations=research_min,
            max_invocations=research_max,
        ),
    ]


def react_pattern(*, think_max: int = 5) -> Requirements:
    """Section 9: ReAct — think first and again after *every* tool call."""
    return [
        ConditionalRequirement(
            ThinkTool,
            force_at_step=1,
            force_after=Tool,  # any tool
            min_invocations=1,
            max_invocations=think_max,
            consecutive_allowed=False,
        ),
    ]


def approved_research() -> Requirements:
    """Section 10: think first; Wikipedia only with human approval, at most once."""
    return [
        ConditionalRequirement(
            ThinkTool,
            force_at_step=1,
            min_invocations=1,
            max_invocations=2,
            consecutive_allowed=False,
        ),
        AskPermissionRequirement(WikipediaTool),
        ConditionalRequirement(
            WikipediaTool,
            only_after=[ThinkTool],
            min_invocations=0,
            max_invocations=1,
        ),
    ]
