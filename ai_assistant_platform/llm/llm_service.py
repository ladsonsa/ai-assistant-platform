from ai_assistant_platform.config.settings import (
    LLM_PROVIDER,
)

from ai_assistant_platform.llm.provider_factory import (
    ProviderFactory,
)


class LLMService:
    """
    Central access point for all LLM interactions.

    Responsibilities:
        - Select the configured provider.
        - Forward requests to the provider.
        - Centralize retries and fallback logic.
        - Provide a stable interface for agents.
    """

    def __init__(self) -> None:
        self.provider = ProviderFactory.create(LLM_PROVIDER)

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate a response using the configured provider.

        Args:
            messages:
                Chat messages formatted according
                to the provider interface.

        Returns:
            Generated text response.
        """

        return self.provider.generate_response(messages)
