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
    ) -> dict:
        """
        Generate a localized response for a mathematical result.
        """

        prompt = build_writer_prompt(
            result=self._format_result(
                result,
            ),
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
    ) -> dict:
        """
        Generate a localized error message.
        """

        prompt = f"""
User message:
{user_message}

Internal error:
{error}

Rules:
- Detect the user's language.
- Reply in the same language.
- Be concise.
- Never expose implementation details.
- Return only the final answer.
"""

        return self.llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate multilingual mathematical error messages."
                    ),
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
        Format a numerical result for presentation.
        """

        if float(value).is_integer():
            return str(
                int(value),
            )

        return str(value)
