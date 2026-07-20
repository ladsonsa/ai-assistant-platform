from ai_assistant_platform.tools.expression_evaluator import (
    ExpressionEvaluator,
)

_evaluator = ExpressionEvaluator()


def evaluate(
    expression: str,
) -> float:
    """
    Evaluate a complete mathematical expression.

    Args:
        expression:
            Mathematical expression containing numbers,
            parentheses and the operators +, -, * and /.

    Returns:
        The numerical result of the evaluated expression.
    """

    return ExpressionEvaluator().evaluate(
        expression,
    )


def add(
    number_1: float,
    number_2: float,
) -> float:
    """
    Add two numbers.
    """

    return number_1 + number_2


def subtract(
    number_1: float,
    number_2: float,
) -> float:
    """
    Subtract the second number from the first.
    """

    return number_1 - number_2


def multiply(
    number_1: float,
    number_2: float,
) -> float:
    """
    Multiply two numbers.
    """

    return number_1 * number_2


def divide(
    number_1: float,
    number_2: float,
) -> float:
    """
    Divide the first number by the second.

    Raises:
        ZeroDivisionError:
            If the divisor is zero.
    """

    if number_2 == 0:
        raise ZeroDivisionError("Division by zero.")

    return number_1 / number_2
