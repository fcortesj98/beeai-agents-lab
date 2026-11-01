"""Agent builders.

- ``base``: :func:`build_agent`, the shared RequirementAgent factory
- ``requirements``: reusable requirement sets (sections 6-10)
- ``cybersecurity``: the analyst in six capability levels (sections 5-10)
- ``math_assistant``: agent using the custom calculator tool (section 11)
- ``travel``: multi-agent travel planner with handoffs (section 12)
"""

from beeai_lab.agents.base import build_agent
from beeai_lab.agents.cybersecurity import AnalystVariant, build_cybersecurity_analyst
from beeai_lab.agents.math_assistant import build_math_assistant
from beeai_lab.agents.travel import TravelTeam, build_travel_team

__all__ = [
    "AnalystVariant",
    "TravelTeam",
    "build_agent",
    "build_cybersecurity_analyst",
    "build_math_assistant",
    "build_travel_team",
]
