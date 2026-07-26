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
