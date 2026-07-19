from openai import (
    OpenAI,
    RateLimitError,
)

from ai_assistant_platform.config.settings import (
    FREQUENCY_PENALTY,
    MAX_TOKENS,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    PRESENCE_PENALTY,
    TEMPERATURE,
    TOP_P,
)
from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI implementation of the BaseLLMProvider interface.
    """

    model_name = OPENAI_MODEL

    def __init__(self) -> None:

        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> dict:
        """
        Generate a response using the OpenAI Chat Completions API.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=TEMPERATURE,
                max_completion_tokens=MAX_TOKENS,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY_PENALTY,
                presence_penalty=PRESENCE_PENALTY,
            )

            usage = response.usage

            return {
                "content": response.choices[0].message.content or "",
                "usage": {
                    "provider": "openai",
                    "model": self.model_name,
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS,
                    "top_p": TOP_P,
                    "frequency_penalty": FREQUENCY_PENALTY,
                    "presence_penalty": PRESENCE_PENALTY,
                    "input_tokens": getattr(
                        usage,
                        "prompt_tokens",
                        None,
                    ),
                    "output_tokens": getattr(
                        usage,
                        "completion_tokens",
                        None,
                    ),
                    "total_tokens": getattr(
                        usage,
                        "total_tokens",
                        None,
                    ),
                    "finish_reason": response.choices[0].finish_reason,
                },
            }

        except RateLimitError as exc:
            raise RuntimeError(
                "OpenAI rate limit exceeded. Please try again later."
            ) from exc

        except Exception as exc:
            raise RuntimeError(f"OpenAI provider error: {exc}") from exc
