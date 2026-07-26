def add(
    number_1: float,
    number_2: float,
) -> float:
    """Performs addition of two floating-point numbers.

    Args:
        number_1 (float): The first addend.
        number_2 (float): The second addend.

    Returns:
        float: The sum of number_1 and number_2.

    Raises:
        None
    """
    return number_1 + number_2


def subtract(
    number_1: float,
    number_2: float,
) -> float:
    """Performs subtraction of two floating-point numbers.

    Args:
        number_1 (float): The minuend.
        number_2 (float): The subtrahend.

    Returns:
        float: The difference resulting from subtracting number_2 from number_1.

    Raises:
        None
    """
    return number_1 - number_2


def multiply(
    number_1: float,
    number_2: float,
) -> float:
    """Performs multiplication of two floating-point numbers.

    Args:
        number_1 (float): The multiplicand.
        number_2 (float): The multiplier.

    Returns:
        float: The product of number_1 and number_2.

    Raises:
        None
    """
    return number_1 * number_2


def divide(
    number_1: float,
    number_2: float,
) -> float:
    """Performs division of two floating-point numbers.

    Args:
        number_1 (float): The dividend.
        number_2 (float): The divisor.

    Returns:
        float: The quotient resulting from dividing number_1 by number_2.

    Raises:
        ZeroDivisionError: If number_2 is zero.
    """
    if number_2 == 0:
        raise ZeroDivisionError("Division by zero.")

    return number_1 / number_2
