from abc import ABC
from abc import abstractmethod


class IExpressionEvaluator(ABC):
    """Interface definition for mathematical expression evaluators."""

    @abstractmethod
    def evaluate(
        self,
        expression: str,
    ) -> float:
        """Evaluates a mathematical expression given as a string.

        Args:
            expression (str): The mathematical expression to be evaluated.

        Returns:
            float: The result of the evaluation.
        """
        ...
