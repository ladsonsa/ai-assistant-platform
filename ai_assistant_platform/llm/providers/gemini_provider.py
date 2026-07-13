from google import genai

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


class GeminiProvider(BaseLLMProvider):
    """
    Gemini implementation of the BaseLLMProvider interface.
    """

    model_name = GEMINI_MODEL

    def __init__(self) -> None:
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

        return {
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
