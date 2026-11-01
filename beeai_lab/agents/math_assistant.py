"""Math assistant agent that uses the custom calculator tool (lab section 11)."""

from __future__ import annotations

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.backend import ChatModel

from beeai_lab.agents.base import build_agent
from beeai_lab.prompts.system_prompts import MATH_ASSISTANT
from beeai_lab.tools.calculator import SimpleCalculatorTool


def build_math_assistant(llm: ChatModel) -> RequirementAgent:
    return build_agent(llm, MATH_ASSISTANT, tools=[SimpleCalculatorTool()])
