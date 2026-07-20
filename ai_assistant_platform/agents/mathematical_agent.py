# ai_assistant_platform/agents/mathematical_agent.py

from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)


class MathematicalAgent:
    """An agent responsible for executing mathematical tasks using an injected evaluator."""

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
        """
        Evaluate a mathematical expression.

        Args:
            expression:
                Canonical mathematical expression.

        Returns:
            Result of the evaluated expression.

        Raises:
            ValueError:
                If the expression contains unsupported syntax.

            ZeroDivisionError:
                If a division by zero is attempted.
        """

        return evaluate_expression(
            expression=expression,
        )

