from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)

logger = get_logger(__name__)


def evaluate(
    expression: str,
) -> float:
    """Evaluates a complete mathematical expression string using the expression evaluator tool.

    Args:
        expression (str): The mathematical expression to be evaluated.

    Returns:
        float: The numerical result of the evaluation.

    Raises:
        ValueError: If the expression is invalid.
        ZeroDivisionError: If a division by zero occurs during evaluation.
    """
    logger.debug(
        "Evaluating complete expression expression=%s",
        expression,
    )

    result = evaluate_expression(
        expression=expression,
    )

    logger.info(
        "Expression evaluated result=%s",
        result,
    )

    return result


def add(
    number_1: float,
    number_2: float,
) -> float:
    """Performs addition of two floating-point numbers.

    Args:
        number_1 (float): The first addend.
        number_2 (float): The second addend.

    Returns:
        float: The sum of number_1 and number_2.

    Raises:
        None
    """
    result = number_1 + number_2
    logger.debug(
        "Addition executed left=%s right=%s result=%s",
        number_1,
        number_2,
        result,
    )
    return result


def subtract(
    number_1: float,
    number_2: float,
) -> float:
    """Performs subtraction of two floating-point numbers.

    Args:
        number_1 (float): The minuend.
        number_2 (float): The subtrahend.

    Returns:
        float: The difference resulting from subtracting number_2 from number_1.

    Raises:
        None
    """
    result = number_1 - number_2
    logger.debug(
        "Subtraction executed left=%s right=%s result=%s",
        number_1,
        number_2,
        result,
    )
    return result


def multiply(
    number_1: float,
    number_2: float,
) -> float:
    """Performs multiplication of two floating-point numbers.

    Args:
        number_1 (float): The multiplicand.
        number_2 (float): The multiplier.

    Returns:
        float: The product of number_1 and number_2.

    Raises:
        None
    """
    result = number_1 * number_2
    logger.debug(
        "Multiplication executed left=%s right=%s result=%s",
        number_1,
        number_2,
        result,
    )
    return result


def divide(
    number_1: float,
    number_2: float,
) -> float:
    """Performs division of two floating-point numbers.

    Args:
        number_1 (float): The dividend.
        number_2 (float): The divisor.

    Returns:
        float: The quotient resulting from dividing number_1 by number_2.

    Raises:
        ZeroDivisionError: If number_2 is zero.
    """
    if number_2 == 0:
        logger.warning(
            "Division by zero attempted left=%s right=%s",
            number_1,
            number_2,
        )
        raise ZeroDivisionError("Division by zero.")

    result = number_1 / number_2
    logger.debug(
        "Division executed left=%s right=%s result=%s",
        number_1,
        number_2,
        result,
    )
    return result
