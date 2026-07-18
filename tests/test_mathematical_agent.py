import pytest

from ai_assistant_platform.agents.mathematical_agent import (
    MathematicalAgent,
)


@pytest.fixture
def agent() -> MathematicalAgent:
    return MathematicalAgent()


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 2", 4.0),
        ("10 - 3", 7.0),
        ("6 * 8", 48.0),
        ("20 / 4", 5.0),
        ("(2 + 3) * 4", 20.0),
        ("2 + 3 * 4", 14.0),
    ],
)
def test_execute_returns_expected_result(
    agent: MathematicalAgent,
    expression: str,
    expected: float,
) -> None:
    assert agent.execute(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("-5", -5.0),
        ("+5", 5.0),
        ("-(-5)", 5.0),
        ("3.5 + 2.5", 6.0),
    ],
)
def test_execute_supports_unary_and_decimal_operations(
    agent: MathematicalAgent,
    expression: str,
    expected: float,
) -> None:
    assert agent.execute(expression) == expected


def test_execute_raises_zero_division_error(
    agent: MathematicalAgent,
) -> None:
    with pytest.raises(ZeroDivisionError):
        agent.execute("10 / 0")


@pytest.mark.parametrize(
    "expression",
    [
        "",
        "abc",
        "2 + hello",
        "__import__('os')",
        "eval('2+2')",
        "sum([1])",
        "lambda x: x",
        "2 ** 8",
        "10 % 3",
        "5 // 2",
    ],
)
def test_execute_raises_value_error_for_invalid_expression(
    agent: MathematicalAgent,
    expression: str,
) -> None:
    with pytest.raises(ValueError):
        agent.execute(expression)


def test_execute_returns_float(
    agent: MathematicalAgent,
) -> None:
    result = agent.execute("2 + 2")

    assert isinstance(result, float)