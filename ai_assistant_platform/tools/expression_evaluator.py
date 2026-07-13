# ai_assistant_platform/tools/expression_evaluator.py

import ast
import operator


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_expression(
    expression: str,
) -> float:
    """
    Safely evaluate a mathematical expression.

    Supported:
        - Parentheses
        - +, -, *, /
        - Unary + and -

    Raises:
        ValueError:
            If the expression contains unsupported syntax.

        ZeroDivisionError:
            If division by zero occurs.
    """

    try:
        tree = ast.parse(
            expression,
            mode="eval",
        )

    except SyntaxError as exc:
        raise ValueError("Invalid mathematical expression.") from exc

    return float(
        _evaluate_node(
            tree.body,
        )
    )


def _evaluate_node(
    node: ast.AST,
) -> float:

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
            _evaluate_node(
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

        left = _evaluate_node(
            node.left,
        )

        right = _evaluate_node(
            node.right,
        )

        if (
            operator_type is ast.Div
            and right == 0
        ):
            raise ZeroDivisionError("Division by zero.")

        return _OPERATORS[operator_type](
            left,
            right,
        )

    raise ValueError(
        "Invalid mathematical expression."
    )