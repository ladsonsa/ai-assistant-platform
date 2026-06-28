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
    agents and response generation.
    """

    def __init__(
        self,
        mathematical_agent: MathematicalAgent,
        writer_agent: WriterAgent,
    ) -> None:

        self.mathematical_agent = mathematical_agent
        self.writer_agent = writer_agent

    def process_message(
        self,
        user_message: str,
        conversation_history: list[dict],
    ) -> str:

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
