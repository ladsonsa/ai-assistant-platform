# ai_assistant_platform/tools/math_operations.py

from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)


def evaluate(
    expression: str,
) -> float:
    """
    Evaluates a complete mathematical expression.
    """

    return evaluate_expression(
        expression,
    )


def add(
    number_1: float,
    number_2: float,
) -> float:

    return number_1 + number_2


def subtract(
    number_1: float,
    number_2: float,
) -> float:

    return number_1 - number_2


def multiply(
    number_1: float,
    number_2: float,
) -> float:

    return number_1 * number_2


def divide(
    number_1: float,
    number_2: float,
) -> float:

    if number_2 == 0:
        raise ZeroDivisionError("Division by zero.")

    return number_1 / number_2
