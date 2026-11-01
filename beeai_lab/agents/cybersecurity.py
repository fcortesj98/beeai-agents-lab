"""The cybersecurity analyst used in lab sections 5-10.

The lab rebuilds the same agent six times, adding one capability each time.
Here those six versions are entries in a table: each variant names its tools
and its requirement set, and one builder creates any of them.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.tools import Tool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.think import ThinkTool

from beeai_lab.agents import requirements as req
from beeai_lab.agents.base import build_agent
from beeai_lab.prompts.system_prompts import CYBERSECURITY_ANALYST


class AnalystVariant(str, Enum):
    MINIMAL = "minimal"  # section 5
    RESEARCH = "research"  # section 6
    REASONING = "reasoning"  # section 7
    CONTROLLED = "controlled"  # section 8
    REACT = "react"  # section 9
    SECURE = "secure"  # section 10


def _think_and_research() -> list[Tool[Any, Any, Any]]:
    return [ThinkTool(), WikipediaTool()]


@dataclass(frozen=True)
class VariantSpec:
    tools: Callable[[], list[Tool[Any, Any, Any]]]
    requirements: Callable[[], req.Requirements] = field(default=list)
    track_tools: bool = True


VARIANTS: dict[AnalystVariant, VariantSpec] = {
    AnalystVariant.MINIMAL: VariantSpec(tools=list, track_tools=False),
    AnalystVariant.RESEARCH: VariantSpec(lambda: [WikipediaTool()], req.limited_research),
    AnalystVariant.REASONING: VariantSpec(_think_and_research, req.limited_reasoning_and_research),
    AnalystVariant.CONTROLLED: VariantSpec(_think_and_research, req.think_then_research),
    AnalystVariant.REACT: VariantSpec(_think_and_research, req.react_pattern),
    AnalystVariant.SECURE: VariantSpec(_think_and_research, req.approved_research),
}


def build_cybersecurity_analyst(
    llm: ChatModel,
    variant: AnalystVariant | str = AnalystVariant.MINIMAL,
    instructions: str = CYBERSECURITY_ANALYST,
) -> RequirementAgent:
    """Create the analyst agent at the requested capability level."""
    spec = VARIANTS[AnalystVariant(variant)]
    return build_agent(
        llm,
        instructions,
        tools=spec.tools(),
        requirements=spec.requirements(),
        track_tools=spec.track_tools,
    )
