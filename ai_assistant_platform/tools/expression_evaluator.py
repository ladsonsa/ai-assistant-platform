import ast
import operator

from ai_assistant_platform.config.logging_config import (
    get_logger,
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


def evaluate_expression(
    expression: str,
) -> float:
    logger.debug(
        "Evaluating mathematical expression expression=%s",
        expression,
    )

    try:
        tree = ast.parse(
            expression,
            mode="eval",
        )
    except SyntaxError as exc:
        logger.warning(
            "Invalid mathematical expression syntax expression=%s",
            expression,
        )
        raise ValueError("Invalid mathematical expression.") from exc

    result = float(
        _evaluate_node(
            tree.body,
        )
    )

    logger.debug(
        "Expression evaluated successfully expression=%s result=%s",
        expression,
        result,
    )

    return result


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
            logger.warning(
                "Unsupported constant detected node_type=%s",
                type(node).__name__,
            )
            raise ValueError("Only numeric constants are allowed.")

        return float(node.value)

    if isinstance(
        node,
        ast.UnaryOp,
    ):
        operator_type = type(node.op)

        if operator_type not in _OPERATORS:
            logger.warning(
                "Unsupported unary operator operator=%s",
                operator_type.__name__,
            )
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
            logger.warning(
                "Unsupported binary operator operator=%s",
                operator_type.__name__,
            )
            raise ValueError("Unsupported operator.")

        left = _evaluate_node(
            node.left,
        )

        right = _evaluate_node(
            node.right,
        )

        if operator_type is ast.Div and right == 0:
            logger.warning("Division by zero detected")
            raise ZeroDivisionError("Division by zero.")

        return _OPERATORS[operator_type](
            left,
            right,
        )

    logger.warning(
        "Invalid AST node detected node_type=%s",
        type(node).__name__,
    )
    raise ValueError("Invalid mathematical expression.")
