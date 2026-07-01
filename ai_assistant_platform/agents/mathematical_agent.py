from ai_assistant_platform.tools.math_operations import (
    add,
    divide,
    multiply,
    subtract,
)


class MathematicalAgent:
    """
    A specialized agent responsible for executing mathematical operations.

    This agent determines whether a user request contains a supported
    mathematical operation and delegates the computation to the
    appropriate mathematical tool.

    The agent is intentionally limited to operation selection and
    execution. It does not perform natural language generation,
    communicate with language models, or format responses for end users.

    Attributes:
        OPERATIONS (dict[str, Callable[[float, float], float]]):
            Mapping between operation names and their corresponding
            mathematical functions.

        KEYWORDS (dict[str, list[str]]):
            Mapping of supported operations to the keywords used for
            intent detection in user messages.
    """

    OPERATIONS = {
        "addition": add,
        "subtraction": subtract,
        "multiplication": multiply,
        "division": divide,
    }

    KEYWORDS = {
        "addition": ["add", "+", "plus"],
        "subtraction": ["subtract", "-", "minus"],
        "multiplication": ["multiply", "*", "times"],
        "division": ["divide", "/", "divided by"],
    }

    def can_handle(
        self,
        user_message: str,
    ) -> bool:
        """
        Determine whether the agent can process a user request.

        The method performs a keyword-based search to identify whether
        the provided message contains a supported mathematical operation.

        Args:
            user_message: The user's input message.

        Returns:
            True if the message contains at least one supported
            mathematical keyword; otherwise, False.
        """

        message = user_message.lower()

        return any(
            keyword in message
            for keywords in self.KEYWORDS.values()
            for keyword in keywords
        )

    def execute(
        self,
        operation: str,
        number_1: float,
        number_2: float,
    ) -> float:
        """
        Execute a supported mathematical operation.

        The requested operation is resolved through the internal
        operation registry and delegated to the corresponding
        mathematical function.

        Args:
            operation: Name of the mathematical operation to execute.
            number_1: The first operand.
            number_2: The second operand.

        Returns:
            The result of the mathematical operation.

        Raises:
            ValueError: If the provided operation is not supported.
        """

        if operation not in self.OPERATIONS:
            raise ValueError(f"Unsupported operation: {operation}")

        return self.OPERATIONS[operation](
            number_1,
            number_2,
        )
