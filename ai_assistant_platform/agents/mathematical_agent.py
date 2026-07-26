from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)

logger = get_logger(__name__)


class MathematicalAgent:
    """
    Executes validated mathematical expressions.
    """

    def execute(
        self,
        expression: str,
    ) -> float:
        logger.info(
            "Executing mathematical expression expression=%s",
            expression,
        )

        result = evaluate_expression(
            expression=expression,
        )

        logger.info(
            "Mathematical expression executed result=%s",
            result,
        )

        return result
