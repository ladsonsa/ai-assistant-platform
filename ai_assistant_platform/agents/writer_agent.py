from ai_assistant_platform.llm.llm_service import (
    LLMService,
)

from ai_assistant_platform.prompts.writer_prompt import (
    build_writer_prompt,
)


class WriterAgent:
    """
    Generates the final response presented to the user.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self.llm_service = llm_service

    def generate_response(
        self,
        result: float,
        language: str,
    ) -> str:
        """
        Generate a natural language response for a mathematical result.

        Args:
            result:
                Calculated mathematical result.

            language:
                ISO 639-1 language code detected by ContextResolver.

        Returns:
            Natural response in the detected language.
        """

        prompt = build_writer_prompt(
            result=self._format_result(result),
            language=language,
        )

        return self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": ("You are a multilingual mathematical assistant."),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

    def generate_error_response(
        self,
        user_message: str,
        error: str,
    ) -> str:
        """
        Generate a localized error message.

        Args:
            user_message:
                Original user message.

            error:
                Internal error.

        Returns:
            Friendly error message.
        """

        prompt = f"""
User language:
{user_message}

Internal error:
{error}

Rules:
- Respond in the same language as the user.
- Be concise.
- Never expose internal implementation details.
- Return only the final answer.
"""

        return self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": ("You generate multilingual error messages."),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

    def _format_result(
        self,
        value: float,
    ) -> str:
        """
        Format numbers for display.
        """

        if value.is_integer():
            return str(int(value))

        return str(value)
