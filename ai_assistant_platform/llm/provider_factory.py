from ai_assistant_platform.llm.providers.openai_provider import (
    OpenAIProvider,
)

from ai_assistant_platform.llm.providers.gemini_provider import (
    GeminiProvider,
)

from ai_assistant_platform.llm.providers.ollama_provider import (
    OllamaProvider,
)


class ProviderFactory:

    PROVIDERS = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "ollama": OllamaProvider,
    }

    @classmethod
    def create(
        cls,
        provider_name: str,
    ):
        provider = cls.PROVIDERS.get(provider_name.lower())

        if provider is None:
            raise ValueError(f"Unsupported provider: {provider_name}")

        return provider()
