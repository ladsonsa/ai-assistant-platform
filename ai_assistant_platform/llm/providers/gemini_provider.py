from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)


class GeminiProvider(BaseLLMProvider):

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        raise NotImplementedError("Gemini provider not implemented yet.")
