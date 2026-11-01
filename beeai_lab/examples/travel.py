"""Section 12 — multi-agent travel planner (replaces ``t12.py``)."""

from __future__ import annotations

from beeai_lab.agents.travel import build_travel_team
from beeai_lab.examples.base import ExampleOptions
from beeai_lab.llm import agent_llm
from beeai_lab.prompts.queries import TRAVEL_QUERY
from beeai_lab.utils import console


async def travel_planner(options: ExampleOptions) -> None:
    team = build_travel_team(agent_llm(options.model), require_approval=options.require_approval)
    result = await team.coordinator.run(options.query or TRAVEL_QUERY)
    console.labeled("📋 Comprehensive Travel Plan", result.answer.text)
