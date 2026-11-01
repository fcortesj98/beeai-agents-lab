"""Section 11 — agent with a custom calculator tool (replaces ``t11.py``)."""

from __future__ import annotations

from beeai_lab.agents.math_assistant import build_math_assistant
from beeai_lab.examples.base import ExampleOptions
from beeai_lab.llm import agent_llm
from beeai_lab.prompts.queries import MATH_QUERIES
from beeai_lab.utils import console


async def calculator_agent(options: ExampleOptions) -> None:
    agent = build_math_assistant(agent_llm(options.model))
    queries = [options.query] if options.query else MATH_QUERIES
    for query in queries:
        result = await agent.run(query)
        console.exchange(query, result.answer.text)
