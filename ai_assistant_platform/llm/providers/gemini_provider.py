from google import genai

from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
)
from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)

logger = get_logger(__name__)


class GeminiProvider(BaseLLMProvider):
    """
    Gemini implementation of the BaseLLMProvider interface.
    """

    model_name = GEMINI_MODEL

    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not configured.")
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        logger.info(
            "Initializing Gemini provider model=%s",
            self.model_name,
        )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
        )

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> dict:
        """
        Generate a response using the Gemini API.
        """

        logger.debug(
            "Sending request to Gemini model=%s messages=%d",
            self.model_name,
            len(messages),
        )

        try:
            prompt = self._build_prompt(
                messages,
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "max_output_tokens": MAX_TOKENS,
                },
            )

            usage = getattr(
                response,
                "usage_metadata",
                None,
            )

            result = {
                "content": getattr(
                    response,
                    "text",
                    "",
                ),
                "usage": {
                    "provider": "gemini",
                    "model": self.model_name,
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS,
                    "top_p": TOP_P,
                    "input_tokens": (
                        getattr(
                            usage,
                            "prompt_token_count",
                            None,
                        )
                        if usage
                        else None
                    ),
                    "output_tokens": (
                        getattr(
                            usage,
                            "candidates_token_count",
                            None,
                        )
                        if usage
                        else None
                    ),
                    "total_tokens": (
                        getattr(
                            usage,
                            "total_token_count",
                            None,
                        )
                        if usage
                        else None
                    ),
                    "finish_reason": getattr(
                        response,
                        "finish_reason",
                        None,
                    ),
                },
            }

            logger.info(
                "Gemini response received model=%s finish_reason=%s",
                self.model_name,
                result["usage"]["finish_reason"],
            )

            return result

        except Exception as exc:
            logger.exception(
                "Gemini provider error model=%s",
                self.model_name,
            )
            raise RuntimeError(f"Gemini provider error: {exc}") from exc

    def _build_prompt(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Convert OpenAI chat messages into a Gemini prompt.
        """

        prompt_parts: list[str] = []

        for message in messages:
            prompt_parts.append(f"{message['role'].capitalize()}: {message['content']}")

        prompt_parts.append("Assistant:")

        return "\n\n".join(
            prompt_parts,
        )
