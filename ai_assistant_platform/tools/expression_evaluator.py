import ast
import operator

from ai_assistant_platform.tools.interfaces.expression_evaluator import (
    IExpressionEvaluator,
)

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class ExpressionEvaluator(IExpressionEvaluator):
    """A safe evaluator for mathematical expressions using abstract syntax trees."""

    def evaluate(
        self,
        expression: str,
    ) -> float:
        """Parses and evaluates a mathematical expression string safely.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The calculated result of the expression.

        Raises:
            ValueError: If the expression contains a syntax error or invalid syntax.
        """

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

        except SyntaxError as exc:
            raise ValueError("Invalid mathematical expression.") from exc

        return float(
            self._evaluate_node(
                tree.body,
            )
        )

    def _evaluate_node(
        self,
        node: ast.AST,
    ) -> float:
        """Recursively evaluates an AST node into a concrete numeric outcome.

        Args:
            node (ast.AST): The abstract syntax tree node to process.

        Returns:
            float: The numeric outcome evaluated from the node.

        Raises:
            ValueError: If the node contains non-numeric constants, unsupported
                operators, or an unparseable structural pattern.
            ZeroDivisionError: If a division by zero operation is detected.
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
