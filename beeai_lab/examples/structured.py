"""Section 4 — structured output with a Pydantic schema (replaces ``t4.py``)."""

from __future__ import annotations

from beeai_framework.backend import SystemMessage, UserMessage

from beeai_lab.examples.base import ExampleOptions
from beeai_lab.llm import structured_llm
from beeai_lab.prompts.queries import BUSINESS_PLAN_QUERY
from beeai_lab.prompts.system_prompts import BUSINESS_CONSULTANT
from beeai_lab.schemas import BusinessPlan


def print_business_plan(plan: BusinessPlan) -> None:
    print("\n🚀 AI-Generated Business Plan:")
    print(f"💡 Business Name: {plan.business_name}")
    print(f"🎯 Elevator Pitch: {plan.elevator_pitch}")
    print(f"👥 Target Market: {plan.target_market}")
    print(f"⭐ Unique Value Proposition: {plan.unique_value_proposition}")
    print(f"💰 Revenue Streams: {', '.join(plan.revenue_streams)}")
    print(f"💵 Startup Costs: {plan.startup_costs}")
    print("🔑 Key Success Factors:")
    for factor in plan.key_success_factors:
        print(f"  - {factor}")


async def generate_business_plan(idea: str, model: str | None = None) -> BusinessPlan:
    """Ask the model for a business plan and validate it against the schema."""
    llm = structured_llm(model)
    response = await llm.create_structure(
        schema=BusinessPlan,
        messages=[SystemMessage(content=BUSINESS_CONSULTANT), UserMessage(content=idea)],
    )
    # create_structure returns a plain dict; validating gives typed attribute access.
    return BusinessPlan.model_validate(response.object)


async def structured_output(options: ExampleOptions) -> None:
    idea = options.query or BUSINESS_PLAN_QUERY
    print(f"User: {idea}")
    plan = await generate_business_plan(idea, options.model)
    print_business_plan(plan)
