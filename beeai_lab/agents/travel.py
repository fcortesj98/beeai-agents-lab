"""Multi-agent travel planner (lab section 12).

Three specialist agents are wrapped as ``HandoffTool``s and given to a
coordinator agent, which decides whom to consult and merges their answers.

    Travel Coordinator ──► DestinationResearch       (Wikipedia + Think)
                       ├─► WeatherPlanning           (OpenMeteo + Think)
                       └─► LanguageCulturalGuidance  (Wikipedia + Think)
"""

from __future__ import annotations

from dataclasses import dataclass

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.ask_permission import AskPermissionRequirement
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.backend import ChatModel
from beeai_framework.tools.handoff import HandoffTool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.weather import OpenMeteoTool

from beeai_lab.agents.base import build_agent
from beeai_lab.prompts import system_prompts as sp

# Handoff tool names — also used by the coordinator's permission requirement.
DESTINATION_HANDOFF = "DestinationResearch"
WEATHER_HANDOFF = "WeatherPlanning"
LANGUAGE_HANDOFF = "LanguageCulturalGuidance"
HANDOFF_NAMES = [DESTINATION_HANDOFF, WEATHER_HANDOFF, LANGUAGE_HANDOFF]


# --- Specialists -------------------------------------------------------------
def build_destination_expert(llm: ChatModel) -> RequirementAgent:
    return build_agent(
        llm,
        sp.DESTINATION_EXPERT,
        tools=[WikipediaTool(), ThinkTool()],
        requirements=[
            ConditionalRequirement(
                ThinkTool, force_at_step=1, min_invocations=1, max_invocations=5, consecutive_allowed=False
            ),
            ConditionalRequirement(
                WikipediaTool,
                only_after=[ThinkTool],
                min_invocations=1,
                max_invocations=4,
                consecutive_allowed=False,
            ),
        ],
    )


def build_travel_meteorologist(llm: ChatModel) -> RequirementAgent:
    return build_agent(
        llm,
        sp.TRAVEL_METEOROLOGIST,
        tools=[OpenMeteoTool(), ThinkTool()],
        requirements=[
            ConditionalRequirement(ThinkTool, force_at_step=1, min_invocations=1, max_invocations=2),
            ConditionalRequirement(OpenMeteoTool, only_after=[ThinkTool], min_invocations=1, max_invocations=1),
        ],
    )


def build_language_culture_expert(llm: ChatModel) -> RequirementAgent:
    return build_agent(
        llm,
        sp.LANGUAGE_CULTURE_EXPERT,
        tools=[WikipediaTool(), ThinkTool()],
        requirements=[
            ConditionalRequirement(
                ThinkTool, force_at_step=1, min_invocations=1, max_invocations=3, consecutive_allowed=False
            ),
        ],
    )


# --- Coordinator -------------------------------------------------------------
@dataclass
class TravelTeam:
    coordinator: RequirementAgent
    destination_expert: RequirementAgent
    meteorologist: RequirementAgent
    language_expert: RequirementAgent


def build_travel_team(llm: ChatModel, *, require_approval: bool = True) -> TravelTeam:
    """Create the three specialists and the coordinator that delegates to them.

    ``require_approval=True`` (the lab's behavior) asks you in the terminal
    before each handoff to a specialist.
    """
    destination = build_destination_expert(llm)
    weather = build_travel_meteorologist(llm)
    language = build_language_culture_expert(llm)

    handoffs = [
        HandoffTool(
            destination,
            name=DESTINATION_HANDOFF,
            description=(
                "Consult our Destination Research Expert for comprehensive information about "
                "travel destinations, attractions, and practical travel guidance."
            ),
        ),
        HandoffTool(
            weather,
            name=WEATHER_HANDOFF,
            description=(
                "Consult our Travel Meteorologist for weather forecasts, climate analysis, and "
                "weather-appropriate travel recommendations."
            ),
        ),
        HandoffTool(
            language,
            name=LANGUAGE_HANDOFF,
            description=(
                "Consult our Language & Cultural Expert for essential phrases, cultural etiquette, "
                "and communication guidance for respectful travel."
            ),
        ),
    ]

    requirements = [ConditionalRequirement(ThinkTool, consecutive_allowed=False)]
    if require_approval:
        requirements.append(AskPermissionRequirement(HANDOFF_NAMES))

    coordinator = build_agent(
        llm, sp.TRAVEL_COORDINATOR, tools=[*handoffs, ThinkTool()], requirements=requirements
    )
    return TravelTeam(coordinator, destination, weather, language)
