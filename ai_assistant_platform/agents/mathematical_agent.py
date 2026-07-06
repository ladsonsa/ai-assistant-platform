from ai_assistant_platform.tools.math_operations import (
    add,
    divide,
    multiply,
    subtract,
)


class MathematicalAgent:
    """
    Agent responsible for executing basic mathematical operations.

    This class delegates mathematical calculations to the corresponding
    operation functions, providing a single entry point for arithmetic
    execution.

    Supported operations:
        - addition
        - subtraction
        - multiplication
        - division
    """

    def __init__(self):
        self.operations = {
            "addition": add,
            "subtraction": subtract,
            "multiplication": multiply,
            "division": divide,
        }

    def execute(
        self,
        operation: str,
        number_1: float,
        number_2: float,
    ) -> float:
        """
        Execute the requested mathematical operation.

        Args:
            operation:
                Canonical operation name.
            number_1:
                First operand.
            number_2:
                Second operand.

        Returns:
            The result of the mathematical operation.

        Raises:
            ValueError:
                If the requested operation is not supported.
        """

        func = self.operations.get(operation)

        if func is None:
            raise ValueError(f"Unsupported operation: {operation}")

        return func(number_1, number_2)
