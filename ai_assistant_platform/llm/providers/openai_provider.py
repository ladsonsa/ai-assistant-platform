from openai import OpenAI

from ai_assistant_platform.config.settings import (
    MODEL_NAME,
    OPENAI_API_KEY,
)

from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)


class OpenAIProvider(BaseLLMProvider):

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )

        return response.choices[0].message.content or ""
