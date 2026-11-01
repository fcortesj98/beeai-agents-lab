"""Sections 5-10 — one cybersecurity analyst, six capability levels.

Replaces ``t5.py`` … ``t10.py``. All six examples send the same query to the
same persona so you can compare what each added capability changes.
"""

from __future__ import annotations

from beeai_lab.agents.cybersecurity import AnalystVariant, build_cybersecurity_analyst
from beeai_lab.examples.base import ExampleOptions, ExampleRunner
from beeai_lab.llm import agent_llm
from beeai_lab.prompts.queries import CYBERSECURITY_QUERY
from beeai_lab.utils import console

RESULT_LABELS: dict[AnalystVariant, str] = {
    AnalystVariant.MINIMAL: "💬 Pure LLM Analysis",
    AnalystVariant.RESEARCH: "📖 Research-Enhanced Analysis",
    AnalystVariant.REASONING: "🧠 Reasoning + Research Analysis",
    AnalystVariant.CONTROLLED: "🔧 Controlled Execution Analysis",
    AnalystVariant.REACT: "🔁 ReAct Analysis",
    AnalystVariant.SECURE: "🛡️ Security-Approved Analysis",
}


async def run_analyst(variant: AnalystVariant, options: ExampleOptions) -> str:
    agent = build_cybersecurity_analyst(agent_llm(options.model), variant)
    result = await agent.run(options.query or CYBERSECURITY_QUERY)
    console.labeled(RESULT_LABELS[variant], result.answer.text)
    return result.answer.text


def runner_for(variant: AnalystVariant) -> ExampleRunner:
    async def _run(options: ExampleOptions) -> None:
        await run_analyst(variant, options)

    return _run
