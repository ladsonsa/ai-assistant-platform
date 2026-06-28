from ai_assistant_platform.tools.math_operations import (
    add,
    divide,
    multiply,
    subtract,
)


class MathematicalAgent:
    """
    Specialized agent responsible for mathematical operations.

    This agent acts as an abstraction layer between the
    orchestration layer and the mathematical tools.

    Responsibilities:
        - Select the appropriate mathematical tool.
        - Execute calculations through tools.
        - Return calculation results.

    Limitations:
        - Does not generate user-facing responses.
        - Does not answer general knowledge questions.
        - Does not perform calculations using LLM reasoning.
    """

    def solve(
        self,
        operation: str,
        number_1: float,
        number_2: float,
    ) -> float:
        """
        Execute a mathematical operation using the corresponding tool.

        Args:
            operation: Operation identifier.
            number_1: First operand.
            number_2: Second operand.

        Returns:
            Result of the mathematical operation.

        Raises:
            ValueError: If the operation is not supported.
        """

        operations = {
            "addition": add,
            "subtraction": subtract,
            "multiplication": multiply,
            "division": divide,
        }

        if operation not in operations:
            raise ValueError(
                f"Unsupported operation: {operation}"
            )

        return operations[operation](
            number_1,
            number_2,
        )