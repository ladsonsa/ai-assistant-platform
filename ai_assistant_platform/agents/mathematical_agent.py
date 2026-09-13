from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.tools.interfaces.expression_evaluator import (
    IExpressionEvaluator,
)

logger = get_logger(__name__)


class MathematicalAgent:
    """Executes validated mathematical expressions using an expression evaluator.

    Attributes:
        _evaluator (IExpressionEvaluator): The evaluator instance used to compute mathematical expressions.
    """

    def __init__(
        self,
        evaluator: IExpressionEvaluator,
    ) -> None:
        """Initializes the MathematicalAgent with an expression evaluator.

        Args:
            evaluator (IExpressionEvaluator): The evaluator implementation to be used for calculations.

        Returns:
            None

        Raises:
            None
        """
        self._evaluator = evaluator

    def execute(
        self,
        expression: str,
    ) -> float:
        """Executes and evaluates the given mathematical expression string.

        Args:
            expression (str): The mathematical expression to execute.

        Returns:
            float: The numerical result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid.
            ZeroDivisionError: If division by zero occurs during evaluation.
        """
        logger.info(
            "Executing mathematical expression expression=%s",
            expression,
        )

        result = self._evaluator.evaluate(
            expression=expression,
        )

        logger.info(
            "Mathematical expression executed result=%s",
            result,
        )

        return result
