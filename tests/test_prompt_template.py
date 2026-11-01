import pytest

from beeai_lab.prompts import MissingTemplateVariableError, SimplePromptTemplate
from beeai_lab.prompts.queries import PROJECT_EVALUATION_TEMPLATE, PROJECT_SCENARIOS


def test_renders_all_placeholders():
    t = SimplePromptTemplate("Hi {{name}}, welcome to {{ place }}.")
    assert t.render({"name": "Ana", "place": "BeeAI"}) == "Hi Ana, welcome to BeeAI."


def test_literal_braces_are_preserved():
    # The lab's str.format-based version raised on templates like this one.
    t = SimplePromptTemplate('Return JSON like {"score": 1} for {{project}}')
    assert t.render({"project": "X"}) == 'Return JSON like {"score": 1} for X'


def test_missing_variable_is_reported():
    with pytest.raises(MissingTemplateVariableError, match="timeline"):
        SimplePromptTemplate("{{project}} {{timeline}}").render({"project": "X"})


def test_lab_scenarios_fill_the_lab_template():
    t = SimplePromptTemplate(PROJECT_EVALUATION_TEMPLATE)
    for scenario in PROJECT_SCENARIOS:
        rendered = t.render(scenario)
        assert "{{" not in rendered
        assert scenario["project_name"] in rendered
