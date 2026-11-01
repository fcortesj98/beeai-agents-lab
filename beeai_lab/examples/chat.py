"""Sections 2-3 — basic chat and prompt templates (replace ``t2.py``, ``t3.py``)."""

from __future__ import annotations

from beeai_framework.backend import SystemMessage, UserMessage

from beeai_lab.examples.base import ExampleOptions
from beeai_lab.llm import chat_llm
from beeai_lab.prompts import SimplePromptTemplate
from beeai_lab.prompts.queries import BUSINESS_IDEA_QUERY, PROJECT_EVALUATION_TEMPLATE, PROJECT_SCENARIOS
from beeai_lab.prompts.system_prompts import CREATIVE_ASSISTANT
from beeai_lab.utils import console


async def basic_chat(options: ExampleOptions) -> None:
    """Send a system + user message to a chat model and print the reply."""
    llm = chat_llm(options.model)
    question = options.query or BUSINESS_IDEA_QUERY
    response = await llm.create(
        messages=[SystemMessage(content=CREATIVE_ASSISTANT), UserMessage(content=question)]
    )
    console.exchange(question, response.get_text_content(), user_label="User", bot_label="Assistant")


async def prompt_templates(options: ExampleOptions) -> None:
    """Render one template with several scenarios and evaluate each with the model.

    ``--query`` is ignored here: the inputs are the scenarios in ``prompts/queries.py``.
    """
    llm = chat_llm(options.model)
    template = SimplePromptTemplate(PROJECT_EVALUATION_TEMPLATE)

    for i, scenario in enumerate(PROJECT_SCENARIOS, 1):
        console.section(f"Project Evaluation {i}: {scenario['project_name']}")
        prompt = template.render(scenario)
        console.labeled("📝 Rendered prompt", prompt)

        response = await llm.create(messages=[UserMessage(content=prompt)])
        console.labeled("🤖 LLM response", response.get_text_content())
