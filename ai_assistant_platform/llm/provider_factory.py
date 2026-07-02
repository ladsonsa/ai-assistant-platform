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
    """
    Factory responsible for creating language model provider instances.

    This factory maps provider identifiers to their corresponding
    implementations and instantiates the requested provider.

    Attributes:
        PROVIDERS (dict[str, type]):
            Mapping between provider names and their implementation
            classes.
    """

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
        """
        Create an instance of the requested language model provider.

        Args:
            provider_name:
                Name of the provider to instantiate.

        Returns:
            An initialized language model provider instance.

        Raises:
            ValueError:
                If the specified provider is not supported.
        """

        provider = cls.PROVIDERS.get(provider_name.lower())

        if provider is None:
            raise ValueError(f"Unsupported provider: {provider_name}")

        return provider()
