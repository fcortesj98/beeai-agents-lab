"""Build every agent and tool without calling a model.

These tests need ``beeai-framework`` installed but no API keys: ChatModel
objects are created with dummy credentials and never invoked.
"""

import asyncio

import pytest

pytest.importorskip("beeai_framework")

from beeai_framework.agents.experimental import RequirementAgent  # noqa: E402

from beeai_lab.agents import AnalystVariant, build_cybersecurity_analyst, build_math_assistant, build_travel_team  # noqa: E402
from beeai_lab.agents.travel import HANDOFF_NAMES  # noqa: E402
from beeai_lab.config import get_settings  # noqa: E402
from beeai_lab.examples import EXAMPLES, get_example  # noqa: E402
from beeai_lab.llm import create_chat_model  # noqa: E402
from beeai_lab.tools.calculator import CalculatorInput, SimpleCalculatorTool  # noqa: E402


@pytest.fixture(autouse=True)
def _dummy_credentials(monkeypatch):
    monkeypatch.setenv("WATSONX_API_KEY", "test")
    monkeypatch.setenv("WATSONX_PROJECT_ID", "test")
    monkeypatch.setenv("WATSONX_URL", "https://example.invalid")
    monkeypatch.setenv("OPENAI_API_KEY", "test")


@pytest.fixture
def llm():
    return create_chat_model(get_settings().agent)


@pytest.mark.parametrize("variant", list(AnalystVariant))
def test_every_analyst_variant_builds(llm, variant):
    assert isinstance(build_cybersecurity_analyst(llm, variant), RequirementAgent)


def test_math_assistant_builds(llm):
    assert isinstance(build_math_assistant(llm), RequirementAgent)


@pytest.mark.parametrize("approval", [True, False])
def test_travel_team_builds(llm, approval):
    team = build_travel_team(llm, require_approval=approval)
    tool_names = {t.name for t in team.coordinator._tools}
    assert set(HANDOFF_NAMES) <= tool_names


def test_gpt5_skips_temperature():
    assert get_settings().structured.temperature is None
    create_chat_model("openai:gpt-5-nano")  # must not raise


def test_calculator_tool_runs():
    async def _call():
        return await SimpleCalculatorTool().run(CalculatorInput(expression="(10 + 5) * 3 - 7"))

    out = asyncio.run(_call())
    text = out.get_text_content()
    assert "Result: 38.0" in text and "Mixed" in text


def test_registry_lookup():
    assert len(EXAMPLES) == 12
    assert get_example("5") is get_example("05") is get_example("t5") is get_example("minimal-agent")
    with pytest.raises(KeyError):
        get_example("99")
