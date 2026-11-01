import pytest

from beeai_lab.tools.arithmetic import CalculationError, evaluate


@pytest.mark.parametrize(
    ("expr", "value", "label"),
    [
        ("15 + 27", 42.0, "Addition"),
        ("144 / 12", 12.0, "Division"),
        ("8 * 9", 72.0, "Multiplication"),
        ("(10 + 5) * 3 - 7", 38.0, "Mixed (Addition, Multiplication, Subtraction)"),
        ("-4 + 10", 6.0, "Addition"),
        ("3.5", 3.5, "Basic Arithmetic"),
    ],
)
def test_valid_expressions(expr, value, label):
    result = evaluate(expr)
    assert result.value == value
    assert result.operation_label == label


@pytest.mark.parametrize(
    "expr",
    [
        "9 ** 9 ** 9",  # exponent: would hang the lab's eval-based version
        "7 // 2",
        "__import__('os')",
        "abs(-1)",
        "1 +",
        "",
        "x + 1",
    ],
)
def test_rejected_expressions(expr):
    with pytest.raises(CalculationError):
        evaluate(expr)


def test_division_by_zero():
    with pytest.raises(CalculationError, match="Division by zero"):
        evaluate("1 / (2 - 2)")
