from openai import OpenAI, RateLimitError

from ai_assistant_platform.config.settings import (
    MODEL_NAME,
    OPENAI_API_KEY,
)

from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)


class OpenAIProvider(BaseLLMProvider):
    """
    Language model provider for OpenAI's Chat Completions API.

    This class implements the BaseLLMProvider interface using OpenAI's
    SDK to generate responses from chat-based language models.

    Attributes:
        client (OpenAI):
            Authenticated OpenAI client used to communicate with the API.
    """

    def __init__(self) -> None:
        """
        Initialize the OpenAI provider.

        Creates an authenticated OpenAI client using the configured API key.
        """

        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate a response using OpenAI's Chat Completions API.

        Args:
            messages:
                A sequence of chat messages formatted according to the
                OpenAI Chat Completions API specification.

        Returns:
            The text content of the model's response. Returns an empty
            string if no content is returned by the API.
        """

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
            )

            return response.choices[0].message.content

        except RateLimitError as exc:
            raise RuntimeError("OpenAI rate limit exceeded.") from exc
