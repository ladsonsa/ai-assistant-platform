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
    Safely evaluates a basic mathematical expression.

    Supported:
        - Parentheses
        - + - * /
        - Unary + and -

    Raises:
        ValueError:
            Invalid expression.

        ZeroDivisionError:
            Division by zero.
    """

    tree = ast.parse(
        expression,
        mode="eval",
    )

    return float(
        _evaluate_node(
            tree.body,
        )
    )


def _evaluate_node(
    node,
):

    if isinstance(
        node,
        ast.Constant,
    ):

        if isinstance(
            node.value,
            (
                int,
                float,
            ),
        ):
            return node.value

        raise ValueError("Invalid constant.")

    if isinstance(
        node,
        ast.Num,
    ):
        return node.n

    if isinstance(
        node,
        ast.UnaryOp,
    ):

        operator_type = type(node.op)

        if operator_type not in _OPERATORS:
            raise ValueError("Unsupported operator.")

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

        if operator_type is ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero.")

        return _OPERATORS[operator_type](
            left,
            right,
        )

    raise ValueError("Invalid mathematical expression.")
