from ai_assistant_platform.agents.mathematical_agent import (
    MathematicalAgent,
)

from ai_assistant_platform.agents.writer_agent import (
    WriterAgent,
)

import re


class ChatbotOrchestrator:
    """
    Central orchestration layer responsible for coordinating
    specialized agents and managing the request processing flow.

    Responsibilities:
        - Analyze incoming user requests.
        - Route requests to the appropriate agent.
        - Extract mathematical operations and operands.
        - Coordinate interaction between agents.
        - Return the final response to the caller.

    Limitations:
        - Does not perform mathematical calculations directly.
        - Does not generate user-facing responses directly.
        - Does not communicate with LLM providers.
    """

    def __init__(
        self,
        mathematical_agent: MathematicalAgent,
        writer_agent: WriterAgent,
    ) -> None:
        """
        Initialize orchestrator dependencies.

        Args:
            mathematical_agent:
                Specialized agent responsible for mathematical
                operations.

            writer_agent:
                Specialized agent responsible for generating
                user-friendly responses.
        """

        self.mathematical_agent = mathematical_agent
        self.writer_agent = writer_agent

    def process_message(
        self,
        user_message: str,
        conversation_history: list[dict],
    ) -> str:
        """
        Process a user message and coordinate the execution flow.

        The orchestrator determines whether the request should be
        handled by the mathematical agent or directly by the writer
        agent.

        Args:
            user_message:
                Message received from the user.

            conversation_history:
                Complete conversation history used to provide
                context for response generation.

        Returns:
            Final response generated for the user.

        Raises:
            ValueError:
                If the mathematical request contains invalid
                or unsupported data.
        """

        if self.mathematical_agent.can_handle(user_message):

            operation = self._extract_operation(user_message)

            number_1, number_2 = self._extract_numbers(user_message)

            math_result = self.mathematical_agent.execute(
                operation=operation,
                number_1=number_1,
                number_2=number_2,
            )

            response = self.writer_agent.generate_response(
                user_message=user_message,
                context=math_result,
            )

        else:

            response = self.writer_agent.generate_response(
                user_message=user_message,
                context=conversation_history,
            )

        return response

    def _extract_numbers(
        self,
        user_message: str,
    ) -> tuple[float, float]:
        """
        Extract numerical operands from the user message.

        Args:
            user_message:
                Original message sent by the user.

        Returns:
            Tuple containing the two extracted operands.

        Raises:
            ValueError:
                If fewer than two numbers are found in the message.
        """

        numbers = re.findall(
            r"-?\d+\.?\d*",
            user_message,
        )

        if len(numbers) < 2:
            raise ValueError("At least two numbers are required.")

        return (
            float(numbers[0]),
            float(numbers[1]),
        )

    def _extract_operation(
        self,
        user_message: str,
    ) -> str:
        """
        Identify the mathematical operation requested by the user.

        Supported operations:
            - addition
            - subtraction
            - multiplication
            - division

        Args:
            user_message:
                Original message sent by the user.

        Returns:
            Internal operation identifier used by the
            mathematical agent.

        Raises:
            ValueError:
                If the requested operation is not supported.
        """

        message = user_message.lower()

        if any(keyword in message for keyword in ["add", "+", "plus"]):
            return "addition"

        if any(keyword in message for keyword in ["subtract", "-", "minus"]):
            return "subtraction"

        if any(keyword in message for keyword in ["multiply", "*", "times"]):
            return "multiplication"

        if any(keyword in message for keyword in ["divide", "/", "divided by"]):
            return "division"

        raise ValueError("Unsupported operation.")
