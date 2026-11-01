"""A custom BeeAI tool: a simple calculator (lab section 11)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.tools import StringToolOutput, Tool, ToolRunOptions

from beeai_lab.tools.arithmetic import CalculationError, evaluate


class CalculatorInput(BaseModel):
    """Input model for basic mathematical calculations."""

    expression: str = Field(
        description=(
            "Mathematical expression using +, -, *, / "
            "(e.g., '10 + 5', '20 - 8', '4 * 6', '15 / 3')"
        )
    )


class SimpleCalculatorTool(Tool[CalculatorInput, ToolRunOptions, StringToolOutput]):
    """A simple calculator tool for basic arithmetic: add, subtract, multiply, divide."""

    name = "SimpleCalculator"
    description = (
        "Performs basic arithmetic calculations: addition (+), subtraction (-), "
        "multiplication (*), and division (/)."
    )
    input_schema = CalculatorInput

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(namespace=["tool", "calculator", "basic"], creator=self)

    async def _run(
        self, input: CalculatorInput, options: ToolRunOptions | None, context: RunContext
    ) -> StringToolOutput:
        try:
            result = evaluate(input.expression)
        except CalculationError as exc:
            return StringToolOutput(f"❌ Calculation Error: {exc}")
        except Exception as exc:  # never crash the agent loop
            return StringToolOutput(f"❌ Unexpected Error: {exc}")

        return StringToolOutput(
            "🧮 Simple Calculator\n"
            f"Expression: {result.expression}\n"
            f"Result: {result.value}\n"
            f"Operation: {result.operation_label}"
        )
