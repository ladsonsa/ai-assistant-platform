from ai_assistant_platform.tools.math_operations import (
    add,
    divide,
    multiply,
    subtract,
)


class MathematicalAgent:
    """
    Specialized agent responsible for mathematical operations.

    Responsibilities:
        - Identify mathematical requests.
        - Select the correct mathematical tool.
        - Execute calculations through tools.

    Limitations:
        - Does not generate responses for users.
        - Does not communicate with LLM providers.
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
        Determine whether this agent can process
        the user request.
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
        Execute a mathematical operation using tools.
        """

        if operation not in self.OPERATIONS:
            raise ValueError(f"Unsupported operation: {operation}")

        return self.OPERATIONS[operation](
            number_1,
            number_2,
        )
