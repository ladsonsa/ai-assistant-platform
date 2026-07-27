from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.llm.llm_service import (
    LLMService,
)
from ai_assistant_platform.prompts.writer_prompt import (
    build_writer_prompt,
)

logger = get_logger(__name__)


class WriterAgent:
    """
    Generates the final response presented to the user.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self._llm_service = llm_service
        logger.info("WriterAgent initialized")

    def generate_response(
        self,
        result: float,
        language: str,
    ) -> dict:
        """
        Generate a localized response for a mathematical result.
        """

        formatted_result = self._format_result(
            result,
        )

        logger.debug(
            "Generating user response result=%s language=%s",
            formatted_result,
            language,
        )

        prompt = build_writer_prompt(
            result=formatted_result,
            language=language,
        )

        response = self._llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": "You are a multilingual mathematical assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        logger.info(
            "User response generated language=%s",
            language,
        )

        return {
            "content": response.get(
                "content", ""
            ),  # ou response["content"] dependendo do seu serviço de LLM
            "usage": response.get("usage", {}),
        }

    def generate_error_response(
        self,
        user_message: str,
        error: str,
    ) -> dict:
        """
        Generate a localized error message.
        """

        logger.warning(
            "Generating localized error response error=%s",
            error,
        )

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

        response = self._llm_service.generate_response(
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

        logger.info("Localized error response generated")

        return response

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
