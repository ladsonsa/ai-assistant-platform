# ai_assistant_platform/agents/mathematical_agent.py

from ai_assistant_platform.tools.expression_evaluator import (
    evaluate_expression,
)


class MathematicalAgent:
    """
    Executes validated mathematical expressions.
    """

    def execute(
        self,
        expression: str,
    ) -> float:
        return evaluate_expression(expression)
