def add(
    number_1: float,
    number_2: float,
) -> float:
    """
    Perform an addition operation.

    Args:
        number_1: First operand.
        number_2: Second operand.

    Returns:
        Sum of both operands.
    """

    return number_1 + number_2


def subtract(
    number_1: float,
    number_2: float,
) -> float:
    """
    Perform a subtraction operation.

    Args:
        number_1: First operand.
        number_2: Second operand.

    Returns:
        Difference between operands.
    """

    return number_1 - number_2


def multiply(
    number_1: float,
    number_2: float,
) -> float:
    """
    Perform a multiplication operation.

    Args:
        number_1: First operand.
        number_2: Second operand.

    Returns:
        Product of both operands.
    """

    return number_1 * number_2


def divide(
    number_1: float,
    number_2: float,
) -> float:
    """
    Perform a division operation.

    Args:
        number_1: Dividend.
        number_2: Divisor.

    Returns:
        Division result.

    Raises:
        ValueError:
            If division by zero is attempted.
    """

    if number_2 == 0:
        raise ValueError(
            "Division by zero is not allowed."
        )

    return number_1 / number_2