"""Registry of runnable examples, one per lab section."""

from __future__ import annotations

from beeai_lab.agents.cybersecurity import AnalystVariant
from beeai_lab.examples import analyst, calculator, chat, environment, structured, travel
from beeai_lab.examples.base import Example, ExampleOptions

EXAMPLES: list[Example] = [
    Example("01", "environment", "Environment check", "Credentials & model configuration", "t1.py", environment.run),
    Example("02", "basic-chat", "Your first AI conversation", "ChatModel.create()", "t2.py", chat.basic_chat),
    Example("03", "prompt-templates", "Prompt templates", "Reusable {{variable}} prompts", "t3.py", chat.prompt_templates),
    Example("04", "structured-output", "Structured output", "create_structure() + Pydantic", "t4.py", structured.structured_output),
    Example("05", "minimal-agent", "Your first BeeAI agent", "RequirementAgent, no tools", "t5.py",
            analyst.runner_for(AnalystVariant.MINIMAL)),
    Example("06", "research-agent", "Tool calling", "WikipediaTool + trajectory middleware", "t6.py",
            analyst.runner_for(AnalystVariant.RESEARCH)),
    Example("07", "reasoning-agent", "Add reasoning", "ThinkTool", "t7.py",
            analyst.runner_for(AnalystVariant.REASONING)),
    Example("08", "controlled-agent", "Controlled execution", "ConditionalRequirement ordering/limits", "t8.py",
            analyst.runner_for(AnalystVariant.CONTROLLED)),
    Example("09", "react-agent", "ReAct pattern", "Think after every tool call", "t9.py",
            analyst.runner_for(AnalystVariant.REACT)),
    Example("10", "secure-agent", "Human-in-the-loop", "AskPermissionRequirement", "t10.py",
            analyst.runner_for(AnalystVariant.SECURE), interactive=True),
    Example("11", "calculator-agent", "Custom tool", "Writing a Tool subclass", "t11.py",
            calculator.calculator_agent),
    Example("12", "travel-planner", "Multi-agent travel planner", "HandoffTool coordination", "t12.py",
            travel.travel_planner, interactive=True),
]

_BY_KEY: dict[str, Example] = {}
for _ex in EXAMPLES:
    for _key in (_ex.id, _ex.id.lstrip("0"), _ex.slug, _ex.original_script, _ex.original_script.removesuffix(".py")):
        _BY_KEY[_key.lower()] = _ex


def get_example(key: str) -> Example:
    """Look up an example by number ("5", "05"), slug ("minimal-agent") or lab file ("t5")."""
    try:
        return _BY_KEY[key.strip().lower()]
    except KeyError:
        raise KeyError(f"Unknown example '{key}'. Run `python3.11 -m beeai_lab list` to see options.") from None


__all__ = ["EXAMPLES", "Example", "ExampleOptions", "get_example"]
