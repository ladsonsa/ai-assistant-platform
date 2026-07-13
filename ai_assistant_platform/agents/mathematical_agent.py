# ai_assistant_platform/agents/mathematical_agent.py

from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)


class MathematicalAgent:
    """
    Executes validated mathematical expressions.

    The agent is responsible only for evaluating expressions that have
    already been validated by the ContextResolver.
    """

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
