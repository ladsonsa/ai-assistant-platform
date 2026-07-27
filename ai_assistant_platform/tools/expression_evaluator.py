import ast
import operator

from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.tools.interfaces.expression_evaluator import (
    IExpressionEvaluator,
)

logger = get_logger(__name__)

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class ExpressionEvaluator(IExpressionEvaluator):
    """Evaluates mathematical expression strings safely using Abstract Syntax Trees.

    Attributes:
        None
    """

    def evaluate(
        self,
        expression: str,
    ) -> float:
        """Evaluates a given mathematical expression string and returns the floating-point result.

        Args:
            expression (str): The mathematical expression string to evaluate.

        Returns:
            float: The numerical result of the evaluated expression.

        Raises:
            ValueError: If the expression contains syntax errors or invalid elements.
            ZeroDivisionError: If the evaluation attempts to divide by zero.
        """
        logger.debug(
            "Evaluating expression=%s",
            expression,
        )

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )
        except SyntaxError as exc:
            logger.warning(
                "Invalid expression=%s",
                expression,
            )
            raise ValueError("Invalid mathematical expression.") from exc

        result = float(
            self._evaluate_node(
                tree.body,
            )
        )

        logger.debug(
            "Expression evaluated result=%s",
            result,
        )

        return result

    def _evaluate_node(
        self,
        node: ast.AST,
    ) -> float:
        """Recursively evaluates an abstract syntax tree node for mathematical operations.

        Args:
            node (ast.AST): The AST node to evaluate.

        Returns:
            float: The numerical value resulting from the node evaluation.

        Raises:
            ValueError: If an unsupported constant, unary operator, binary operator, or node type is encountered.
            ZeroDivisionError: If a division by zero occurs.
        """
        if isinstance(
            node,
            ast.Constant,
        ):
            if not isinstance(
                node.value,
                (
                    int,
                    float,
                ),
            ):
                raise ValueError("Only numeric constants are allowed.")

            return float(node.value)

        if isinstance(
            node,
            ast.UnaryOp,
        ):
            operator_type = type(node.op)

            if operator_type not in _OPERATORS:
                raise ValueError("Unsupported unary operator.")

            return _OPERATORS[operator_type](
                self._evaluate_node(
                    node.operand,
                )
            )

        if isinstance(
            node,
            ast.BinOp,
        ):
            operator_type = type(node.op)

            if operator_type not in _OPERATORS:
                raise ValueError("Unsupported operator.")

            left = self._evaluate_node(
                node.left,
            )

            right = self._evaluate_node(
                node.right,
            )

            if operator_type is ast.Div and right == 0:
                raise ZeroDivisionError("Division by zero.")

            return _OPERATORS[operator_type](
                left,
                right,
            )

        raise ValueError("Invalid mathematical expression.")
