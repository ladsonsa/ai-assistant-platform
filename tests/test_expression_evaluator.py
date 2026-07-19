import pytest

from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 2", 4.0),
        ("10 - 3", 7.0),
        ("6 * 8", 48.0),
        ("20 / 4", 5.0),
    ],
)
def test_basic_operations(
    expression: str,
    expected: float,
) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14.0),
        ("10 - 6 / 2", 7.0),
        ("8 + 4 * 2 - 3", 13.0),
        ("100 / 5 + 8", 28.0),
    ],
)
def test_operator_precedence(
    expression: str,
    expected: float,
) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("(2 + 3) * 4", 20.0),
        ("10 / (2 + 3)", 2.0),
        ("((5 + 1) * 3)", 18.0),
        ("(8 - 2) * (10 / 5)", 12.0),
    ],
)
def test_parentheses(
    expression: str,
    expected: float,
) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("-5", -5.0),
        ("+5", 5.0),
        ("-(2 + 3)", -5.0),
        ("+(2 + 3)", 5.0),
        ("-(-5)", 5.0),
    ],
)
def test_unary_operations(
    expression: str,
    expected: float,
) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("3.5 + 2.5", 6.0),
        ("10.5 - 0.5", 10.0),
        ("2.5 * 4", 10.0),
        ("7.5 / 2.5", 3.0),
    ],
)
def test_decimal_numbers(
    expression: str,
    expected: float,
) -> None:
    assert evaluate_expression(expression) == expected


def test_division_by_zero() -> None:
    with pytest.raises(ZeroDivisionError):
        evaluate_expression("10 / 0")


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
        "[1,2,3]",
        "{1:2}",
    ],
)
def test_invalid_expressions(
    expression: str,
) -> None:
    with pytest.raises(ValueError):
        evaluate_expression(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "2 ** 8",
        "10 % 3",
        "5 // 2",
    ],
)
def test_unsupported_operators(
    expression: str,
) -> None:
    with pytest.raises(ValueError):
        evaluate_expression(expression)
