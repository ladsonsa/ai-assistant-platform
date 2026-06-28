from ai_assistant_platform.llm.providers.base_provider import (
    BaseLLMProvider,
)


class OllamaProvider(BaseLLMProvider):

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        raise NotImplementedError("Ollama provider not implemented yet.")
