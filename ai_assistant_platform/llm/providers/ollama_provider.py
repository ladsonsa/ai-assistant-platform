from ollama import Client

from ai_assistant_platform.config.settings import (
    MAX_TOKENS,
    OLLAMA_MODEL,
    TEMPERATURE,
    TOP_P,
)
from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)


class OllamaProvider(BaseLLMProvider):
    """
    Ollama implementation of the BaseLLMProvider interface.
    """

    model_name = OLLAMA_MODEL

    def __init__(self) -> None:
        self.client = Client()

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> dict:
        """
        Generate a response using the local Ollama server.
        """

        try:

            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                options={
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "num_predict": MAX_TOKENS,
                },
            )

            input_tokens = response.get(
                "prompt_eval_count",
            )

            output_tokens = response.get(
                "eval_count",
            )

            return {
                "content": response["message"]["content"],
                "usage": {
                    "provider": "ollama",
                    "model": self.model_name,
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS,
                    "top_p": TOP_P,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": ((input_tokens or 0) + (output_tokens or 0)),
                    "eval_duration": response.get(
                        "eval_duration",
                    ),
                    "load_duration": response.get(
                        "load_duration",
                    ),
                    "prompt_eval_duration": response.get(
                        "prompt_eval_duration",
                    ),
                    "finish_reason": response.get(
                        "done_reason",
                    ),
                },
            }

        except Exception as exc:
            raise RuntimeError(f"Ollama provider error: {exc}") from exc
