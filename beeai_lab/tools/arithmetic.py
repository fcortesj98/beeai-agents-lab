"""Safe arithmetic evaluation, independent of BeeAI so it can be unit-tested.

The lab's calculator used ``eval`` with a character allow-list. That still let
through ``**`` (``9**9**9`` hangs the process) and ``//``. This module parses
the expression with :mod:`ast` and only evaluates ``+ - * /``, unary signs,
parentheses and numbers.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable
from dataclasses import dataclass

_BINARY_OPS: dict[type[ast.operator], tuple[Callable[[float, float], float], str]] = {
    ast.Add: (operator.add, "Addition"),
    ast.Sub: (operator.sub, "Subtraction"),
    ast.Mult: (operator.mul, "Multiplication"),
    ast.Div: (operator.truediv, "Division"),
}
_UNARY_OPS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
MAX_EXPRESSION_LENGTH = 200


class CalculationError(ValueError):
    """Raised for invalid or unsupported expressions."""


@dataclass(frozen=True)
class CalculationResult:
    expression: str
    value: float
    operations: tuple[str, ...]  # e.g. ("Addition", "Multiplication"), in first-seen order

    @property
    def operation_label(self) -> str:
        if not self.operations:
            return "Basic Arithmetic"
        if len(self.operations) == 1:
            return self.operations[0]
        return "Mixed (" + ", ".join(self.operations) + ")"


def evaluate(expression: str) -> CalculationResult:
    """Evaluate a basic arithmetic expression safely."""
    expr = expression.strip()
    if not expr:
        raise CalculationError("Expression is empty")
    if len(expr) > MAX_EXPRESSION_LENGTH:
        raise CalculationError(f"Expression is longer than {MAX_EXPRESSION_LENGTH} characters")
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise CalculationError(f"Invalid arithmetic expression: {exc.msg}") from exc

    seen: list[str] = []

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return float(node.value)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
            return _UNARY_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
            func, label = _BINARY_OPS[type(node.op)]
            left, right = _eval(node.left), _eval(node.right)
            if label not in seen:
                seen.append(label)
            try:
                return func(left, right)
            except ZeroDivisionError as exc:
                raise CalculationError("Division by zero is not allowed") from exc
        raise CalculationError(
            "Only numbers, parentheses and the operators +, -, *, / are allowed"
        )

    value = _eval(tree)
    return CalculationResult(expression=expr, value=value, operations=tuple(seen))
