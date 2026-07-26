from ollama import Client

from ai_assistant_platform.config.logging_config import (
    get_logger,
)
from ai_assistant_platform.config.settings import (
    MAX_TOKENS,
    OLLAMA_MODEL,
    TEMPERATURE,
    TOP_P,
)
from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)

logger = get_logger(__name__)


class OllamaProvider(BaseLLMProvider):
    """
    Ollama implementation of the BaseLLMProvider interface.
    """

    model_name = OLLAMA_MODEL

    def __init__(self) -> None:
        logger.info(
            "Initializing Ollama provider model=%s",
            self.model_name,
        )
        self.client = Client()

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> dict:
        """
        Generate a response using the local Ollama server.
        """

        logger.debug(
            "Sending request to Ollama model=%s messages=%d",
            self.model_name,
            len(messages),
        )

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

            result = {
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

            logger.info(
                "Ollama response received model=%s finish_reason=%s",
                self.model_name,
                result["usage"]["finish_reason"],
            )

            return result

        except Exception as exc:
            logger.exception(
                "Ollama provider error model=%s",
                self.model_name,
            )
            raise RuntimeError(f"Ollama provider error: {exc}") from exc
