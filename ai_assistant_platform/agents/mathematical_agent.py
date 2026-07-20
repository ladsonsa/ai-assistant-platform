from ai_assistant_platform.tools.interfaces.expression_evaluator import (
    IExpressionEvaluator,
)


class MathematicalAgent:
    """An agent responsible for executing mathematical tasks using an injected evaluator.

    Attributes:
        _evaluator (IExpressionEvaluator): The expression evaluator instance
            used to evaluate mathematical expressions.
    """

    def __init__(
        self,
        evaluator: IExpressionEvaluator,
    ) -> None:
        """Initializes the MathematicalAgent with an expression evaluator.

        Args:
            evaluator (IExpressionEvaluator): The concrete evaluator instance
                used to process mathematical expressions.
        """
        self._evaluator = evaluator

    def execute(
        self,
        expression: str,
    ) -> float:
        """Executes the evaluation of a given mathematical expression string.

        Args:
            expression (str): The mathematical expression to be evaluated.

        Returns:
            float: The calculated result of the expression.
        """
        return self._evaluator.evaluate(
            expression=expression,
        )
